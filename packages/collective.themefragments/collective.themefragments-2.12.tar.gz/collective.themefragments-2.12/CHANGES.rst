Changelog
=========

2.12 (2019-07-26)
-----------------

- Add support for Python 3 and Plone 5.2.
  [pbauer]


2.11.1 (2017-10-30)
-------------------

- Fix issue where themefragment tile was unable to render head tiles with
  &_mode=head query parameter as expected
  [datakurre]


2.11 (2017-10-18)
-----------------

- Add 'macros' accessor for fragment view to make fragment view template macros
  accessible and usable e.g. in classic portlets
  [datakurre]

2.10.2 (2017-09-24)
-------------------

- Fix issue where theming was disabled for frament views
  [datakurre]

2.10.1 (2017-09-13)
-------------------

- Fix issue where tile id and url were not accessible from tile fragment templates
  [datakurre]

2.10.0 (2017-08-28)
-------------------

- Add ++themefragment++name -traverser to allow direct use of themefragments as
  views
  [datakurre]

- Add fragment Python module support for fragment tile
  [datakurre]

2.9.0 (2017-08-28)
------------------

- Add support for fragment Python modules (as PEP8 compatible single file
  replacement for fragment methods support in previous versions)
  [datakurre]

- Change to make templates owned by their creator instead to inherit owner from
  their rendered context
  [datakurre]

2.8.0 (2017-08-21)
------------------

- Add traversable @@output_relative_to helper for RichTextValue object to
  support rendering rich text field values in restricted templates
  [datakurre]


2.7.1 (2017-06-13)
------------------

- Fix issue where fragment tile URL did not include selected fragment itself
  [datakurre]


2.7.0 (2017-06-09)
------------------

- Fix issue where add form was unable to use fragment name from request
  [datakurre]

- Fix to filter comments beginning with '#' when reading tile titles
  [datakurre]

- Remove incomplete support for persistent annotation storage for theme
  fragment tiles
  [datakurre]


2.6.1 (2017-04-19)
------------------

- Fix to read fragment name from tile data before selecting cache rule
  [datakurre]


2.6.0 (2017-04-19)
------------------

- Change fragment tile to prefer persistent configuratio over query
  string configuration when choosing the configured fragment
  [datakurre]


2.5.2 (2017-02-27)
------------------

- Fix issue where missing 'fragment' parameter resulted in AttributeError
  [datakurre]


2.5.1 (2017-02-24)
------------------

- Fix issue where failure in default caching ruleset lookup prevented tile ruleset lookup
  [datakurre]


2.5.0 (2017-02-24)
------------------

- Add support for fragment tile -specific caching ruleset configuration
  [datakurre]


2.4.0 (2017-02-03)
------------------

- Add ``manifest.cfg`` based configuration for setting more strict
  permissions per each fragment
  [datakurre]


2.3.1 (2017-02-02)
------------------

- Fix issue where ESI tile rendering used public URLs breaking it
  with HTTPS. Fixed by preferring the real request path before
  virtual host transform.
  [datakurre]


2.3.0 (2017-01-30)
------------------

- Add theme fragment tile to use ESI rendering when ESI rendering
  is enabled in plone.app.blocks; When ESI rendering is enabled, all
  theme fragment tiles will be ESI rendred (it may become configurable
  in the future)
  [datakurre]


2.2.0 (2017-01-25)
------------------

- Add caching of parsed TTW tile schemas with theme policy cache
  [datakurre]


2.1.0 (2017-01-24)
------------------

- Add support for fieldsest in TTW XML schemas with
  plone.app.tiles >= 3.1.0
  [datakurre]


2.0.1 (2017-01-18)
------------------

- Add generic catalog source instance to be usable with TTW XML-schema tiles
  [datakurre]

2.0.0 (2017-01-17)
------------------

- Add support for fragment specific widget traversal on fragment tile forms
  [datakurre]

2.0.0rc5 (2016-12-16)
---------------------

- Add minimal permission field checker for fragment tile schemas
  [datakurre]

2.0.0rc4 (2016-12-15)
---------------------

- Fix to hide fragments with empty title from tile menu
  [datakurre]

2.0.0rc3 (2016-12-15)
---------------------

- Fix issue where fragments didn't render when traversed from a view context
  [datakurre]

2.0.0rc2 (2016-12-14)
---------------------

- Fix issue where fragment was not properly decoded
  [datakurre]

2.0.0rc1 (2016-12-12)
---------------------

- Upgrade Theme fragment tiles with custom scheme to support layout aware
  tile data storage introduced in plone.app.blocks 4.0
  [datakurre]


1.1.0 (2016-12-12)
------------------

- Refactor fragment tile source into fragment tile vocabulary to
  fix compatibility issue with Plone 5.1
  [datakurre]


1.0.1 (2016-02-21)
------------------

- Fix issue where plone:tile -directive was not properly included
  [datakurre]


1.0.0 (2015-09-16)
------------------

- Add fragment tile for plone.app.mosaic
  [datakurre]


0.10.0 (2015-04-03)
-------------------

- Add support for restricted python view methods
  (with fragments/templatename.methodname.py)
  [datakurre]


0.9.0 (2015-04-01)
------------------

- First release based on Martin Aspeli's rejected pull for plone.app.theming.
