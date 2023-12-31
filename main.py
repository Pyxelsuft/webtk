import os
import io
import base64
import sys
import time
import threading
import webtk
import requests  # noqa
from PIL import ImageGrab  # noqa


class WebViewApp:
    def __init__(self) -> None:
        self.wv = webtk.webview.create_webview(debug=False)
        self.wv.set_min_size(320, 200)
        # self.wv.set_size(1024, 768)
        self.wv.bind('py_title', self.set_title_cb)
        self.wv.bind('py_print', self.print_text_cb)
        self.wv.bind('py_stop', self.stop_cb)
        self.wv.bind('py_screen', self.screen_cb)
        self.wv.bind('py_fetch', lambda req_id: threading.Thread(target=self.fetch_cb, args=(req_id, )).start())
        self.wv.set_js_hook(open('test.js').read())
        temp_html = open('test.html').read()
        temp_html = temp_html.replace(
            '<link rel="stylesheet" type="text/css" href="test.css">',
            '<style>' + open('test.css').read() + '</style>'
        )
        temp_html = temp_html.replace('<script src="test.js"></script>', '')
        self.wv.set_html(temp_html)

    def run(self) -> None:
        self.wv.run()

    def fetch_cb(self, req_id: bytes) -> None:
        try:
            json_data = requests.get('https://api.github.com/users/pixelsuft').json()
            resp_data = {
                'fws': json_data['followers'],
                'fwg': json_data['following'],
                'rps': json_data['public_repos']
            }
        except Exception as _err:
            print(f'Failed to fetch github stats ({_err})')
            resp_data = {
                'fws': -1,
                'fwg': -1,
                'rps': -1
            }
        time.sleep(3)  # For fun
        self.wv.response(req_id, resp_data)

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
        if hasattr(self, 'wv'):
            self.wv.destroy()


class BrowserApp:
    def __init__(self) -> None:
        self.port = 2389
        try:
            proc = webtk.chrome.run(
                f'http://127.0.0.1:{self.port}/test.html',
                incognito=True, data_dir='temp_webtk_example_chrome'
            )
        except RuntimeError:
            raise RuntimeError('Failed to run any browser')
        # You can do better communication with custom http server or even websockets, but I'm lazy :)
        threading.Thread(target=webtk.server.run_simple_http_server, args=('127.0.0.1', self.port)).start()
        while proc.poll() is None:
            pass
        os.kill(os.getpid(), 1 if sys.platform == 'win32' else 9)


if __name__ == '__main__':
    try:
        app = WebViewApp()
    except Exception as __err:
        print(f'Failed to use WebView ({__err}), using browser as fallback')
        app = BrowserApp()
    if type(app) == WebViewApp:
        app.run()
