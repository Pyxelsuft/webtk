import os
import sys
import subprocess


def find_mac() -> any:
    default_dir = r'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    if os.path.exists(default_dir):
        return default_dir
    # use mdfind ci to locate Chrome in alternate locations and return the first one
    name = 'Google Chrome.app'
    alternate_dirs = [
        x for x in subprocess.check_output(["mdfind", name], encoding='utf-8').split('\n') if x.endswith(name)
    ]
    if len(alternate_dirs):
        return alternate_dirs[0] + '/Contents/MacOS/Google Chrome'
    return None


def find_chromium_mac() -> any:
    default_dir = r'/Applications/Chromium.app/Contents/MacOS/Chromium'
    if os.path.exists(default_dir):
        return default_dir
    # use mdfind ci to locate Chromium in alternate locations and return the first one
    name = 'Chromium.app'
    alternate_dirs = [
        x for x in subprocess.check_output(["mdfind", name], encoding='utf-8').split('\n') if x.endswith(name)
    ]
    if len(alternate_dirs):
        return alternate_dirs[0] + '/Contents/MacOS/Chromium'
    return None


def find_nix() -> any:
    import whichcraft as wch
    chrome_names = ['chromium-browser',
                    'chromium',
                    'google-chrome',
                    'google-chrome-stable']
    for name in chrome_names:
        chrome = wch.which(name)
        if chrome is not None:
            return chrome
    return None


def find_win() -> any:
    import winreg
    reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'

    for install_type in winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE:
        try:
            reg_key = winreg.OpenKey(install_type, reg_path, 0, winreg.KEY_READ)
            chrome_path = winreg.QueryValue(reg_key, None)
            reg_key.Close()
            if not os.path.isfile(chrome_path):
                continue
        except WindowsError:
            chrome_path = None
        else:
            break
    return chrome_path


def find_chrome() -> any:
    if sys.platform == 'win32':
        return find_win()
    elif sys.platform == 'darwin':
        return find_mac() or find_chromium_mac()
    else:
        return find_nix()


def get_run_args(
        chrome_path: str, url: str = None, new_window: bool = True, incognito: bool = False,
        data_dir: str = None, args: any = None
) -> list:
    result = [chrome_path]
    if url:
        result.append('--app=' + url)
    if new_window:
        result.append('--new-window')
    if incognito:
        result.append('--incognito')
    if data_dir:
        result.append('--user-data-dir=' + data_dir)
    if args:
        result += args
    return result


def run(url: str = None, new_window: bool = True, incognito: bool = False,
        data_dir: str = None, args: any = None) -> subprocess.Popen:
    chrome_path = find_chrome()
    if not chrome_path:
        raise RuntimeError('Failed to find chrome')
    return subprocess.Popen(get_run_args(
        chrome_path, url, new_window, incognito, data_dir, args
    ), stdout=subprocess.PIPE, stderr=sys.stderr, stdin=subprocess.PIPE)
