import os
import sys
import ctypes

if sys.platform == 'win32':
    load_library_func = ctypes.windll.LoadLibrary
    load_library_suffix = 'dll'
else:
    load_library_func = ctypes.CDLL
    load_library_suffix = 'dylib' if sys.platform == 'darwin' else 'so'
load_library_errors = (OSError, ImportError, ModuleNotFoundError, FileNotFoundError)


def load_library(path: str) -> ctypes.CDLL:
    try:
        return load_library_func(path)
    except load_library_errors:
        try:
            return load_library_func(os.path.join(os.getcwd(), path))
        except load_library_errors:
            try:
                import __main__
                return load_library_func(os.path.join(os.path.dirname(__main__.__file__), path))
            except load_library_errors:
                if path.endswith('.' + load_library_suffix):
                    return None  # noqa
                return load_library(path + '.' + load_library_suffix)
