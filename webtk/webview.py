import sys
import json
import ctypes as ctp
from . import utils
from . import binder


webview_t = ctp.c_void_p

WEBVIEW_HINT_NONE = 0
WEBVIEW_HINT_MIN = 1
WEBVIEW_HINT_MAX = 2
WEBVIEW_HINT_FIXED = 3

dispatch_cb = ctp.CFUNCTYPE(None, webview_t, ctp.c_void_p)
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
    def __init__(self, handle: ctp.CDLL) -> None:
        super().__init__(handle)
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


class WebView:
    def __init__(self, handle: ctp.CDLL, debug: bool = False, win_handle: any = None) -> None:
        self.inited = False
        self.encoding = 'utf-8'
        self.dll = WebViewDLL(handle)
        self.wv = self.dll.webview_create(int(debug), win_handle)
        if not self.wv:
            raise RuntimeError('Failed to init WebView')
        temp_ver = self.dll.webview_version()
        tvc = temp_ver.contents
        self.version = (tvc.version.major, tvc.version.minor, tvc.version.patch)
        self.version_str = self.bts(tvc.version_number)
        self.version_pre_release = self.bts(tvc.pre_release)
        self.version_build_metadata = self.bts(tvc.build_metadata)
        self.inited = True

    def set_js_hook(self, js_code: str) -> None:
        self.dll.webview_init(self.wv, self.stb(js_code))

    def eval_js(self, js_code: str) -> None:
        self.dll.webview_eval(self.wv, self.stb(js_code))

    def set_url(self, new_url: str) -> None:
        self.dll.webview_navigate(self.wv, self.stb(new_url))

    def set_html(self, new_url: str) -> None:
        self.dll.webview_set_html(self.wv, self.stb(new_url))

    def set_size(self, new_width: any, new_height: any) -> None:
        self.dll.webview_set_size(self.wv, int(new_width), int(new_height), WEBVIEW_HINT_NONE)

    def set_min_size(self, new_width: any, new_height: any) -> None:
        self.dll.webview_set_size(self.wv, int(new_width), int(new_height), WEBVIEW_HINT_MIN)

    def set_max_size(self, new_width: any, new_height: any) -> None:
        self.dll.webview_set_size(self.wv, int(new_width), int(new_height), WEBVIEW_HINT_MAX)

    def set_fixed_size(self, new_width: any, new_height: any) -> None:
        self.dll.webview_set_size(self.wv, int(new_width), int(new_height), WEBVIEW_HINT_FIXED)

    def set_title(self, new_title: str) -> None:
        self.dll.webview_set_title(self.wv, self.stb(new_title))

    def run(self) -> None:
        self.dll.webview_run(self.wv)

    def stop(self) -> None:
        self.dll.webview_terminate(self.wv)

    def destroy(self) -> None:
        if not self.inited:
            return
        self.inited = False
        self.dll.webview_destroy(self.wv)

    def get_window_handle(self) -> any:
        return self.dll.webview_get_window(self.wv)

    def stb(self, text_to_encode: str, encoding: str = None) -> bytes:
        return text_to_encode.encode(encoding or self.encoding, errors='replace')

    def bts(self, text_to_decode: bytes, encoding: str = None) -> str:
        return text_to_decode.decode(encoding or self.encoding, errors='replace')

    def __del__(self) -> None:
        self.destroy()
        self.dll = None


def create_webview(debug: bool = False, win_handle: any = None) -> WebView:
    if sys.platform == 'win32':
        _temp = utils.load_library('WebView2Loader')
    handle = utils.load_library('webview')
    if not handle:
        raise RuntimeError('Failed to load WevView dll')
    return WebView(handle, debug, win_handle)
