import ctypes


class BaseDLL:
    def __init__(self, dll: ctypes.CDLL) -> None:
        self.dll = dll

    def wrap(self, name: str, args: tuple = (), res: any = None) -> any:
        func = getattr(self.dll, name)
        func.argtypes = args
        func.restype = res
        return func
