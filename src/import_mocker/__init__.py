# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
Provides an easy way to import a module and mock its dependencies in an isolated
way. The mocking of the dependencies will apply only to the current import and
will not affect the global module namespace.
"""

import importlib
import sys
from typing import List
from unittest import mock


class ImportMocker(object):
    """
    A class to mock a set of modules and execute operations (like importing
    another module) within a context  that contains those mocked modules. The
    mocking of the modules will be valid for specific operations and does not
    interfere global module namespace.
    """

    def __init__(self, modules_to_mock: List[str]):
        self._modules_to_mock = modules_to_mock
        self._mocks = {}
        self._orig_import = __import__

    def import_module(self, module_to_import: str):
        """
        Imports `module_to_import` inside a context that that returns the mocked
        modules when they are imported, all other imports will work normally.
        If `module_to_import` was previously imported, then it's reloaded so
        that its imported modules can be mocked again.
        """
        with mock.patch("builtins.__import__", side_effect=self._import_mock):
            if module_to_import in sys.modules:
                return importlib.reload(sys.modules[module_to_import])
            else:
                return importlib.import_module(module_to_import)

    def import_modules(self, modules_to_import: List[str]):
        """
        Uses the same logic of `import_module` but receives a list of module
        names to import and returns a list with the imported modules in the same
        order.
        """
        imported_modules = []
        for module in modules_to_import:
            imported_modules.append(self.import_module(module))
                    
        return imported_modules

    def execute(self, function, *args, **kwargs):
        """
        Executes a function inside a context that returns the mocked modules
        when they are imported, all other imports will work normally.

        This is useful when you are testing code that has `import` statements
        inside a function, and you want to mock those imports.

        IMPORTANT: If a module has been previously imported outside the current
        instance of the `ImportMocker`, it will not be re imported when
        executing the function.
        """
        with mock.patch("builtins.__import__", side_effect=self._import_mock):
            function(*args, **kwargs)

    def get_mocks(self):
        """
        Gets a copy of the dictionary containing all the mocked modules.
        """
        return self._mocks.copy()

    def get_mock(self, mock_name: str):
        """
        Gets the specified mocked module.
        """
        return self._mocks[mock_name]

    def reset_mocks(self):
        """
        Resets all the mocked modules to their original state.
        """
        for _, mock_module in self._mocks.items():
            mock_module.reset_mock()

    def reset_mock(self, mock_name: str):
        """
        Resets the specified mocked module to its original state.
        """
        self._mocks[mock_name].reset_mock()

    def _import_mock(self, name, *args):
        if name in self._modules_to_mock:
            if name not in self._mocks:
                self._mocks[name] = mock.Mock()
            return self._mocks[name]

        return self._orig_import(name, *args)
