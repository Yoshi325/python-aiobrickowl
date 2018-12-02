**Important!** This library is still in an alpha state. Do not even consider it for production code.

A Python AsyncIO Implementation of the BrickOwl API
===================================================

Start with `aiobrickowl.session` and then look for your usecase in `aiobrickowl.shortcuts`. If a shortcut does not exist for your usecase, then progress to the individual module that is named the same as the BrickOwl API root path namespace you are attempting to use.

glossary
--------

shortcuts
    In order to support the complexity offered by the API bindings (while still constricting the types of parameters to match said bindings) the functions are nessiariy complex. In order to provide a better user experience a series of shortcuts have been created that provide versions that are more accessible for often used functionality.

bedding
    As in bedding for a owl's nest, this is the underpinnings of this library. Most usecases will not require direct use fo this module.
