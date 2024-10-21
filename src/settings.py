import json
import os

from steam.webauth import WebAuth

from src.path import LAUNCHER_SETTINGS_FILE_PATH

__all__ = ['DEFAULT_USERS', 'settings', 'save_settings']

DEFAULT_USERS = {
    'thb112259': 'steamok7416',
    'agt8729': 'Apk66433',
}


def _init_settings():
    with LAUNCHER_SETTINGS_FILE_PATH.open('r', encoding='utf-8') as f:
        _settings = json.load(f)

    if 'users' not in _settings:
        _settings['users'] = {}
        for user_name, password in DEFAULT_USERS.items():
            webauth = WebAuth()
            try:
                webauth.login(user_name, password)
            except Exception:
                continue
            _settings['users'][user_name] = {
                'user_name': user_name,
                'password': password,
                'token': webauth.refresh_token,
            }

    if 'mods' not in _settings:
        _settings['mods'] = {}

    if 'download_max_threads' not in _settings:
        _settings['download_max_threads'] = min(32, max(1, (os.cpu_count() or 1) // 2))

    if 'chunk_size' not in _settings:
        _settings['max_chunk_size'] = 1024 * 1024
    with LAUNCHER_SETTINGS_FILE_PATH.open('w', encoding='utf-8') as f:
        json.dump(_settings, f, indent=4, ensure_ascii=False)
    return _settings


settings = _init_settings()


def save_settings():
    with LAUNCHER_SETTINGS_FILE_PATH.open('w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)
