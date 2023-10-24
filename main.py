import sys
import webtk

_temp = None
if sys.platform == 'win32':
    _temp = webtk.utils.load_library('WebView2Loader')
dll = webtk.webview.WebViewDLL(webtk.utils.load_library('webview'))


def cb(a1: bytes, a2: any = None, a3: any = None) -> None:
    print(a1, a2)
    dll.webview_return(wv, a1, 0, b'{"shit":"228"}')


wv = dll.webview_create(1, None)
dll.webview_set_title(wv, b'Hello App')
cb_bind = webtk.webview.bind_cb(cb)
dll.webview_bind(wv, b'my_func', cb_bind, None)
dll.webview_init(wv, open('test.js', 'rb').read())
dll.webview_set_html(wv, open('test.html', 'rb').read())
dll.webview_run(wv)
dll.webview_unbind(wv, b'my_func')
dll.webview_destroy(wv)
