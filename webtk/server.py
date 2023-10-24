import os
import contextlib
import socket
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler, CGIHTTPRequestHandler


def _get_best_family(*address):
    info = socket.getaddrinfo(
        *address,
        type=socket.SOCK_STREAM,
        flags=socket.AI_PASSIVE,
    )
    family, type_, proto, canon_name, sock_addr = next(iter(info))
    return family, sock_addr


class DualStackServer(ThreadingHTTPServer):
    def server_bind(self):
        # suppress exception when protocol is IPv4
        with contextlib.suppress(Exception):
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        return super().server_bind()

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self, directory=os.getcwd())  # noqa


def run_simple_http_server(host: any, port: int, protocol: str = 'HTTP/1.0', is_cgi: bool = False) -> None:
    DualStackServer.address_family, addr = _get_best_family(host, port)
    handler = CGIHTTPRequestHandler if is_cgi else SimpleHTTPRequestHandler
    handler.protocol_version = protocol
    with DualStackServer(addr, handler) as httpd:
        return httpd.serve_forever()
