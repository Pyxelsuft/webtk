import webtk


class WebViewApp:
    def __init__(self) -> None:
        self.wv = webtk.webview.create_webview(debug=True)
        self.wv.set_min_size(320, 200)
        # self.wv.set_size(1024, 768)
        self.wv.bind('py_title', self.set_title_cb)
        self.wv.bind('py_print', self.print_text_cb)
        self.wv.set_js_hook(open('test.js').read())
        self.wv.set_html(open('test.html').read())
        self.wv.run()

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
