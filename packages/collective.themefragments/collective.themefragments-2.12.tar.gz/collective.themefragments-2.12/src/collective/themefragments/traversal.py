# -*- coding: utf-8 -*-
from AccessControl.ZopeGuards import get_safe_globals
from AccessControl.ZopeGuards import guarded_getattr
from collective.themefragments.interfaces import FRAGMENTS_DIRECTORY
from collective.themefragments.utils import getFragmentsSettings
from plone.app.theming.interfaces import THEME_RESOURCE_NAME
from plone.app.theming.utils import isThemeEnabled, getCurrentTheme
from plone.memoize import forever
from plone.memoize import view
from plone.resource.utils import queryResourceDirectory
from Products.CMFCore.utils import getToolByName
from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate
from RestrictedPython import compile_restricted_function
from zExceptions import NotFound
from zExceptions import Unauthorized
from zope.component.hooks import getSite
from zope.browser.interfaces import IBrowserView
from zope.interface import implementer
from zope.publisher.browser import BrowserPage
from zope.publisher.interfaces import IPublishTraverse
from zope.security import checkPermission
from zope.traversing.interfaces import ITraversable
from zope.traversing.namespace import SimpleHandler

import Acquisition
import logging
import six
import types

logger = logging.getLogger('collective.themefragments')


@forever.memoize
def prepare_restricted_function(p, body, name, filename, globalize=None):
    # We just do what they do in PythonScript...
    r = compile_restricted_function(p, body, name, filename, globalize)

    code = r[0]
    errors = r[1]
    warnings = tuple(r[2])

    if errors:
        logger.warning('\n'.join(errors))
        raise SyntaxError()
    elif warnings:
        logger.warning('\n'.join(warnings))

    g = get_safe_globals()
    g['_getattr_'] = guarded_getattr
    g['__debug__'] = __debug__
    g['__name__'] = 'script'
    l = {}
    exec(code, g, l)
    f = list(l.values())[0]

    return f.__code__, g, f.__defaults__ or ()


# noinspection PyPep8Naming
class FragmentView(BrowserPage):
    """View class for template-based views defined in the theme.
    When you traverse to ``.../@@theme-fragment/foobar`` to render the view
    defined in ``fragments/foobar.pt`` in the theme, this becomes the ``view``.
    """

    # Allow bound restricted python methods to call each other
    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, context, request, name, permission, template, owner=None):  # noqa
        # Fix issue where context is a template based view class
        while IBrowserView.providedBy(context):
            context = Acquisition.aq_parent(Acquisition.aq_inner(context))

        super(FragmentView, self).__init__(context, request)
        self.__name__ = name
        self._permission = permission
        self._template = template
        self._owner = owner

    # noinspection PyPep8Naming,PyUnresolvedReferences
    def __getattr__(self, name):
        blacklist = ['im_func', 'func_code', 'index_html']
        if name.startswith('_') or name in blacklist:
            raise AttributeError(name)

        # Check if there is views/<self.__name__>.<name>.py in the theme, if not raise  # noqa
        currentTheme = getCurrentTheme()
        if currentTheme is None:
            raise AttributeError(name)

        themeDirectory = queryResourceDirectory(THEME_RESOURCE_NAME, currentTheme)  # noqa
        if themeDirectory is None:
            raise AttributeError(name)

        script = None

        scriptPath = "%s/%s.py" % (FRAGMENTS_DIRECTORY, self.__name__)
        if themeDirectory.isFile(scriptPath):
            script = themeDirectory.readFile(scriptPath)
            if six.PY3 and isinstance(script, six.binary_type):
                script = script.decode('utf8')
            if 'def {0:}(self'.format(name) in script:
                script += '\n\nreturn {0:s}(self)'.format(name)
            else:
                script = None

        scriptPath = "%s/%s.%s.py" % (FRAGMENTS_DIRECTORY, self.__name__, name)
        if script is None and themeDirectory.isFile(scriptPath):
            script = themeDirectory.readFile(scriptPath)
            if six.PY3 and isinstance(script, six.binary_type):
                script = script.decode('utf8')

        if script is None:
            raise AttributeError(name)

        # Set the default PythonScript bindings as globals
        script_globals = {
            'script': self,
            'context': self.context,
            'container': Acquisition.aq_parent(self.context),
            'traverse_subpath': ''
        }

        # Build re-usable restricted function components like in PythonScript
        try:
            code, g, defaults = prepare_restricted_function(
                'self,*args,**kwargs',
                script or 'pass',
                name,
                scriptPath,
                list(script_globals.keys())
            )
        except SyntaxError:
            raise AttributeError(name)

        # Update globals
        g = g.copy()
        g.update(script_globals)
        g['__file__'] = scriptPath
        func = types.FunctionType(code, g, None, defaults)

        # Return the func as instancemethod
        return types.MethodType(func, self)

    @view.memoize
    def _cook_template(self):
        zpt = ZopePageTemplate(self.__name__, text=self._template)
        if self._owner is not None:
            zpt.changeOwnership(self._owner)
        zpt = zpt.__of__(self.context)
        return zpt

    @property
    def macros(self):
        if not checkPermission(self._permission, self.context):
            raise Unauthorized()
        zpt = self._cook_template()
        return zpt.macros

    def __call__(self, *args, **kwargs):
        if not checkPermission(self._permission, self.context):
            raise Unauthorized()
        zpt = self._cook_template()
        portal_url = getToolByName(self.context, 'portal_url')
        boundNames = {
            'context': self.context,
            'request': self.request,
            'view': self,
            'portal_url': portal_url(),
            'portal': portal_url.getPortalObject(),
        }
        try:
            return zpt._exec(boundNames, args, kwargs)
        except NotFound as e:
            # We don't want 404's for these - they are programming errors
            raise Exception(e)


class OutputRelativeToView(BrowserPage):
    """Implements @@output_relative_to view for RichTextValue to make
    it easier to render RichTextValues properly in restricted context
    """

    def __call__(self, context=None):
        if context is None:
            context = getSite()
        return self.context.output_relative_to(context)


@implementer(IPublishTraverse)
class ThemeFragment(BrowserPage):
    """Implements the ``@@theme-fragment`` traversal view. This allows you to
    traverse to ``.../@@theme-fragment/foobar`` to render as a view the
    template found in ``fragments/foobar.pt`` in the currently active theme,
    either in a URL (publish traversal) or in TAL (path traversal).

    Will raise ``KeyError`` (path traversal) or ``NotFound`` (publish
    traversal) if:

    * No valid theme is active
    * The theme is currently disabled
    * No ``.pt`` file exists
    * TODO: The ``.pt`` file is configured in a ``views.cfg`` file to be
      limited to a specific type of context (by interface or class), and the
      current context does not confirm to this type

    TODO: Will raise ``Unauthorized`` if the ``.pt`` file is configured in a
    ``views.cfg`` file to require a specific permission, and the current
    user does not have this permission.
    """

    def __init__(self, context, request, disable_theming=True):
        super(ThemeFragment, self).__init__(context, request)
        self._disable_theming = disable_theming

    def publishTraverse(self, request, name):
        try:
            return self[name]
        except KeyError:
            raise NotFound(self, name, request)

    def __getitem__(self, name):
        # Make sure a theme is enabled
        if not isThemeEnabled(self.request):
            raise KeyError(name)

        # Check if there is views/<name>.pt in the theme, if not raise
        currentTheme = getCurrentTheme()
        if currentTheme is None:
            raise KeyError(name)

        themeDirectory = queryResourceDirectory(THEME_RESOURCE_NAME, currentTheme)  # noqa
        if themeDirectory is None:
            raise KeyError(name)

        templatePath = "%s/%s.pt" % (FRAGMENTS_DIRECTORY, name,)
        if not themeDirectory.isFile(templatePath):
            raise KeyError(name)

        try:
            owner = themeDirectory[templatePath].getOwner()
        except AttributeError:
            owner = getSite().getOwner()
        template = themeDirectory.readFile(templatePath).decode('utf-8', 'replace')  # noqa

        # Now disable the theme so we don't double-transform
        if self._disable_theming:
            self.request.response.setHeader('X-Theme-Disabled', '1')

        # Get settings to map fragment permissions
        permission = getFragmentsSettings(
            themeDirectory, 'themefragments:permissions').get(name) or 'zope.Public'  # noqa

        return FragmentView(self.context, self.request, name, permission, template, owner)  # noqa


@implementer(ITraversable)
class ThemeFragmentView(SimpleHandler):

    def __init__(self, context, request):
        super(ThemeFragmentView, self).__init__(context)
        self.request = request
        self.traverser = ThemeFragment(context, request, disable_theming=False)

    def traverse(self, name, remaining):
        return self.traverser.publishTraverse(self.request, name)
