import json

from prompt_toolkit.shortcuts import message_dialog


def _init_settings():
    from .dialog import PROMPT_TOOLKIT_DIALOG_TITLE
    from .path import CWD, LAUNCHER_SETTINGS_FILE_PATH, MOD_BOOT_FILES_PATH, MODS_DIR_PATH

    _settings = None

    # 初始化配置文件
    try:
        with LAUNCHER_SETTINGS_FILE_PATH.open('r', encoding='utf-8') as f:
            _settings = json.load(f)
        _old_settings = _settings

        if 'users' not in _settings:
            _settings['users'] = {
                'thb112259': 'steamok7416',
                'agt8729': 'Apk66433',
            }

        if 'mods' not in _settings:
            _settings['mods'] = {}

        if _old_settings != _settings:
            with LAUNCHER_SETTINGS_FILE_PATH.open('w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
    except FileNotFoundError:
        message_dialog(
            PROMPT_TOOLKIT_DIALOG_TITLE,
            f'没有找到启动器配置文件, 请检查当前目录是否是游戏根目录\n{CWD}',
            '退出',
        )
        exit(1)
    except Exception as e:
        raise e

    MODS_DIR_PATH.mkdir(parents=True, exist_ok=True)
    MOD_BOOT_FILES_PATH.mkdir(parents=True, exist_ok=True)
    return _settings


settings = _init_settings()
