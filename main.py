import webtk


class WebViewApp:
    def __init__(self) -> None:
        self.wv = webtk.webview.create_webview(debug=True)
        self.wv.set_min_size(320, 200)
        # self.wv.set_size(1024, 768)
        self.wv.set_title('WebTK Example')
        self.wv.set_js_hook(open('test.js').read())
        self.wv.set_html(open('test.html').read())
        self.wv.run()

    def __del__(self):
        self.wv.destroy()


if __name__ == '__main__':
    WebViewApp()
