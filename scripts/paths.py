import sys
import os


_CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
_PACKAGE_DIRECTORY = _CURRENT_DIRECTORY


def add_packages_to_path():
    sys.path.append(os.path.normpath(_PACKAGE_DIRECTORY))
