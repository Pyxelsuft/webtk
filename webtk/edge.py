import sys
import subprocess


# TODO: check if this works, I don't have Edge


def find() -> any:
    return 'present' if sys.platform == 'win32' else None


def get_run_args(url: str, args: any = None) -> list:
    return ['start', 'microsoft-edge:' + url] + (args or [])


def run(url: str, args: any = None) -> subprocess.Popen:
    edge_path = find()
    if not edge_path:
        raise RuntimeError('Failed to find edge')
    return subprocess.Popen(get_run_args(
        url, args
    ), stdout=subprocess.PIPE, stderr=sys.stderr, stdin=subprocess.PIPE)
