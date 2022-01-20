"""utils"""
import types


def assert_package_installed(module):
    assert isinstance(
        module, types.ModuleType
    ), f"{module} is not installed, try to install it."
