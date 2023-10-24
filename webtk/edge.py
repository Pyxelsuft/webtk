import sys
import subprocess


# TODO: check if this works, I don't have Edge


def find_edge() -> any:
    return 'present' if sys.platform == 'win32' else None


def edge_get_run_args(url: str, args: any = None) -> list:
    return ['start', 'microsoft-edge:' + url] + (args or [])


def run_edge(url: str, args: any = None) -> subprocess.Popen:
    edge_path = find_edge()
    if not edge_path:
        raise RuntimeError('Failed to find edge')
    return subprocess.Popen([
        'start', 'microsoft-edge:' + url
    ] + (args or []), stdout=subprocess.PIPE, stderr=sys.stderr, stdin=subprocess.PIPE)
