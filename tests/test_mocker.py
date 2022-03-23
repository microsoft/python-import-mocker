# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from unittest import mock
from import_mocker import ImportMocker


def test_can_create_import_mocker():
    imocker = ImportMocker([])
    assert imocker is not None


def test_can_mock_single_module():
    # Arrange
    imocker = ImportMocker(["module_b"])

    # Act
    module_a = imocker.import_module("module_a")

    # Assert
    # Verify mocks are being generated for the correct modules
    module_b = imocker.get_mock("module_b")
    assert isinstance(module_b, mock.Mock)
    assert not isinstance(module_a, mock.Mock)

def test_can_mock_multiple_modules():
    # Arrange
    imocker = ImportMocker(["module_c", "module_b"])

    # Act
    module_a = imocker.import_module("module_a")

    # Assert
    # Verify mocks are being generated for the correct modules
    mocked_modules = imocker.get_mocks()
    module_b = mocked_modules["module_b"]
    module_c = mocked_modules["module_c"]
    assert isinstance(module_b, mock.Mock)
    assert isinstance(module_c, mock.Mock)
    assert not isinstance(module_a, mock.Mock)

def test_can_import_multiple_modules():
    # Arrange
    imocker = ImportMocker(["module_c"])

    # Act
    [module_a, module_b] = imocker.import_modules(["module_a", "module_b"])

    # Assert
    # Verify mocks are being generated for the correct modules
    mocked_modules = imocker.get_mocks()
    module_c = mocked_modules["module_c"]
    assert isinstance(module_c, mock.Mock)
    assert not isinstance(module_a, mock.Mock)
    assert not isinstance(module_b, mock.Mock)


def test_can_call_mock_from_single_module():
    # Arrange
    imocker = ImportMocker(["module_b"])
    module_a = imocker.import_module("module_a")

    # Act
    module_a.function_a_that_calls_b()

    # Assert
    # Verify mock gets called correctly
    module_b = imocker.get_mock("module_b")
    module_b.function_b.assert_called_once()

def test_can_call_mock_from_multiple_modules():
    # Arrange
    imocker = ImportMocker(["module_c"])
    [module_a, module_b] = imocker.import_modules(["module_a", "module_b"])

    # Act
    module_a.function_a_that_calls_c()
    module_b.function_b_that_calls_c()

    # Assert
    # Verify mock gets called correctly from multiple modules
    module_c = imocker.get_mock("module_c")
    module_c.function_c.assert_called()
    assert module_c.function_c.call_count == 2


def test_can_reset_single_mock():
    # Arrange
    imocker = ImportMocker(["module_c"])
    [module_a, module_b] = imocker.import_modules(["module_a", "module_b"])

    # Act
    module_a.function_a_that_calls_c()
    module_b.function_b_that_calls_c()

    # Assert
    # Verify mocks are working before and after reset
    module_c = imocker.get_mock("module_c")
    module_c.function_c.assert_called()
    assert module_c.function_c.call_count == 2

    imocker.reset_mock("module_c")
    module_c.function_c.assert_not_called()
    assert module_c.function_c.call_count == 0

def test_can_reset_all_mocks():
    # Arrange
    imocker = ImportMocker(["module_c"])
    [module_a, module_b] = imocker.import_modules(["module_a", "module_b"])

    # Act
    module_a.function_a_that_calls_c()
    module_b.function_b_that_calls_c()

    # Assert
    # Verify mocks are working before and after reset
    module_c = imocker.get_mock("module_c")
    module_c.function_c.assert_called()
    assert module_c.function_c.call_count == 2

    imocker.reset_mocks()
    module_c.function_c.assert_not_called()
    assert module_c.function_c.call_count == 0

def test_can_execute_code_on_dynamically_imported_mock():
    # Arrange
    imocker = ImportMocker(["module_b", "module_c", "module_d"])
    module_a = imocker.import_module("module_a")

    # Act
    module_a.function_a_that_calls_b()
    module_a.function_a_that_calls_c()
    imocker.execute(lambda: module_a.function_a_that_imports_and_calls_d())

    # Assert
    # Verify mocks are executed correctly
    module_b = imocker.get_mock("module_b")
    module_b.function_b.assert_called_once()

    module_c = imocker.get_mock("module_c")
    module_c.function_c.assert_called_once()

    # The module_d mock should have been imported dynamically when using execute()
    module_d = imocker.get_mock("module_d")
    module_d.function_d.assert_called_once()
