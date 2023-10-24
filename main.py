import io
import base64
import webtk
from PIL import ImageGrab


class WebViewApp:
    def __init__(self) -> None:
        self.wv = webtk.webview.create_webview(debug=False)
        self.wv.set_min_size(320, 200)
        # self.wv.set_size(1024, 768)
        self.wv.bind('py_title', self.set_title_cb)
        self.wv.bind('py_print', self.print_text_cb)
        self.wv.bind('py_stop', self.stop_cb)
        self.wv.bind('py_screen', self.screen_cb)
        self.wv.set_js_hook(open('test.js').read())
        self.wv.set_html(open('test.html').read().replace('test.css here please', open('test.css').read()))
        self.wv.run()

    def stop_cb(self, req_id: bytes) -> None:
        self.wv.response(req_id)
        self.wv.stop()

    def screen_cb(self, req_id: bytes) -> None:
        buf = io.BytesIO()
        img = ImageGrab.grab()
        img.save(buf, 'png')
        buf.seek(0)
        self.wv.response(req_id, b'["data:image/png;base64,' + base64.b64encode(buf.read()) + b'"]')

    def set_title_cb(self, req_id: bytes, new_title: str) -> None:
        self.wv.set_title(new_title)
        self.wv.response(req_id)

    def print_text_cb(self, req_id: bytes, *fmt: any) -> None:
        print(*fmt)
        self.wv.response(req_id)

    def __del__(self):
        self.wv.destroy()


if __name__ == '__main__':
    WebViewApp()
