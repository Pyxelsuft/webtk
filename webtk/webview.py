import ctypes
import ctypes as ctp
from . import binder


webview_t = ctp.c_void_p

WEBVIEW_HINT_NONE = 0
WEBVIEW_HINT_MIN = 1
WEBVIEW_HINT_MAX = 2
WEBVIEW_HINT_FIXED = 3

dispatch_cb = ctp.CFUNCTYPE(None, webview_t, ctypes.c_void_p)
bind_cb = ctp.CFUNCTYPE(None, ctp.c_char_p, ctp.c_char_p, ctp.c_void_p)


class WebViewVersion(ctp.Structure):
    _fields_ = [
        ('major', ctp.c_uint),
        ('minor', ctp.c_uint),
        ('patch', ctp.c_uint)
    ]


class WebViewVersionInfo(ctp.Structure):
    _fields_ = [
        ('version', WebViewVersion),
        ('version_number', ctp.c_char * 32),
        ('pre_release', ctp.c_char * 48),
        ('build_metadata', ctp.c_char * 48)
    ]


class WebViewDLL(binder.BaseDLL):
    def __init__(self, dll: ctp.CDLL) -> None:
        super().__init__(dll)
        self.webview_create = self.wrap('webview_create', (ctp.c_int, ctp.c_void_p), webview_t)
        self.webview_destroy = self.wrap('webview_destroy', (webview_t, ))
        self.webview_run = self.wrap('webview_run', (webview_t, ))
        self.webview_terminate = self.wrap('webview_terminate', (webview_t, ))
        self.webview_get_window = self.wrap('webview_get_window', (webview_t, ), ctp.c_void_p)
        self.webview_set_title = self.wrap('webview_set_title', (webview_t, ctp.c_char_p))
        self.webview_set_size = self.wrap('webview_set_size', (webview_t, ctp.c_int, ctp.c_int, ctp.c_int))
        self.webview_navigate = self.wrap('webview_navigate', (webview_t, ctp.c_char_p))
        self.webview_set_html = self.wrap('webview_set_html', (webview_t, ctp.c_char_p))
        self.webview_init = self.wrap('webview_init', (webview_t, ctp.c_char_p))
        self.webview_eval = self.wrap('webview_eval', (webview_t, ctp.c_char_p))
        self.webview_unbind = self.wrap('webview_unbind', (webview_t, ctp.c_char_p))
        self.webview_return = self.wrap('webview_return', (webview_t, ctp.c_char_p, ctp.c_int, ctp.c_char_p))
        self.webview_version = self.wrap('webview_version', (), ctp.POINTER(WebViewVersionInfo))
        self.webview_dispatch = self.wrap('webview_dispatch', (webview_t, dispatch_cb, ctp.c_void_p))
        self.webview_bind = self.wrap('webview_bind', (webview_t, ctp.c_char_p, bind_cb, ctp.c_void_p))
