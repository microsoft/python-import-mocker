# Python Import Mocker

The Python Import Mocker provides an easy way to import a module and mock its
dependencies in an isolated way.
The mocking of the dependencies will apply only to the current import and will
not affect the global module namespace.

## Quick Start

### Install

```bash
pip install import-mocker
```

### Mock imports

```py
from import_mocker import ImportMocker

modules_to_mock = ['B', 'C']
imocker = ImportMocker(modules_to_mock)
A = imocker.import_module('A')
```

### Verify behavior on mocked modules

```py
mocks = imocker.get_mocks()
b_mock = mocks['B']
b_mock.some_method.assert_called()
```

### Reset mocked modules

```py
imocker.reset_mock('B')
imocker.reset_mocks()
```

### Execute code within a mocked module context

This is useful when the code to execute will perform an inline `import`.

```py
imocker.execute(lambda: function_that_calls_inline_import())
```

## Rationale

When unit testing in Python we couldn't find a way to easily mock imports
without affecting the global scope and without having to carefully mock and
de-mock the imported modules.

This was a problem for us because we needed to test some files, and then mock
those same files when testing other files, and we can't control the order in
which the tests are executed. Here is an example:

```py
# ***** SOURCE CODE *****
# FILE: A.py
import B
import C
import D
...

# FILE: B.py
import C
import D
...


# ***** TESTS *****
# FILE: test_a.py
# We need to mock B, and C, and the real version of D
from importlib import reload
from unittest import mock
sys.modules["B"] = mock.Mock()
sys.modules["C"] = mock.Mock()

import D
D = reload(D) # Make sure we get the real module if D was mocked before

import A # this line recursively imports B, C, and D
A = reload(A) # Make sure the correct mocks are used if A was mocked before

...

# FILE: test_b.py
# We need to mock only D, and need the real version of C
from importlib import reload
from unittest import mock
sys.modules["D"] = mock.Mock()

import C # Make sure the correct mocks are used if C was mocked before
C = reload(C)
import B # Make sure the correct mocks are used if B was mocked before
B = reload(B)

```

As it can be seen, this can get very verbose, especially when dependencies start
to grow and we need different configurations for mocking.

This is why we created Python Import Mocker, to greately simplify this process
without having to reinvent the wheel every time. We hope you find this as useful
as we did 😀.

## Example

Following the example given in the [previous section](#Rationale),
here is how the Python Import Mocker would be used:

```py
# ***** SOURCE CODE *****
# FILE: A.py
import B
import C
import D
...

# FILE: B.py
import C
import D
...


# ***** TESTS USING PYTHON IMPORT MOCKER *****
# FILE: test_a.py
# We need to mock B and C
from unittest import mock
from import_mocker import ImportMocker

modules_to_mock = ['B', 'C']
imocker = ImportMocker(modules_to_mock)
A = imocker.import_module('A')
...

def my_test_01():
    # Do something and verify B and C
    imocker.reset_mocks()
    execute_code()
    mocks = imocker.get_mocks()
    b_mock = mocks['B']
    b_mock.some_method.assert_called()
    ...
    
    # Do something else and verify C
    imocker.reset_mock('C')
    execute_mode_code()
    c_mock = imocker.get_mock('C')
    c_mock.some_method.assert_called_once()
    ...
...

# FILE: test_b.py
# We need to mock only D, and need the real version of C
from import_mocker import ImportMocker

modules_to_mock = ['D']
imocker = ImportMocker(modules_to_mock)
B = imocker.import_module('B')
...

```

**Note:** You can find more practical examples in the test files.

## API

These are the functions provided by the `ImportMocker` class.

### `import_module(module_to_import: str)`

Imports `module_to_import` inside a context that that returns the mocked modules
when they are imported, all other imports will work normally.

If `module_to_import` was previously imported, then it's reloaded so that its
imported modules can be mocked again.

### `import_modules(module_to_import: str)`

Uses the same logic of `import_module` but receives a list of module names to
import and returns a list with the imported modules in the same order.

### `execute(function)`

Executes a function inside a context that returns the mocked modules when they
are imported, all other imports will work normally.

This is useful when you are testing code that has `import` statements inside
a function, and you want to mock those imports.

IMPORTANT: If a module has been previously imported outside the current instance
of the `ImportMocker`, it will not be re imported when executing the function.

### `get_mocks()`

Gets a copy of the dictionary containing all the mocked modules.

### `get_mock(mock_name: str)`

Gets the specified mocked module.

### `reset_mocks()`

Resets all the mocked modules to their original state.

### `reset_mock(mock_name: str)`

Resets the specified mocked module to its original state.

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit <https://cla.opensource.microsoft.com>.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
