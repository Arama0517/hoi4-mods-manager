import json
import os

from src.path import LAUNCHER_SETTINGS_FILE_PATH

__all__ = ['DEFAULT_USERS', 'settings', 'save_settings']

DEFAULT_USERS = {
    'thb112259': 'steamok7416',
    'agt8729': 'Apk66433',
}


def _init_settings():
    with LAUNCHER_SETTINGS_FILE_PATH.open('r', encoding='utf-8') as f:
        _settings = json.load(f)

    if 'ssl' not in _settings:
        _settings['ssl'] = True

    if 'users' not in _settings:
        _settings['users'] = {}

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
