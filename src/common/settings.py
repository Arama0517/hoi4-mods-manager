# 美化错误
import json

from prompt_toolkit.shortcuts import message_dialog

from src.common.dialog import PROMPT_TOOLKIT_DIALOG_TITLE
from src.common.path import CWD, LAUNCHER_SETTINGS_FILE_PATH, MOD_BOOT_FILES_PATH, MODS_DIR_PATH

settings = None

# 初始化配置文件
try:
    with LAUNCHER_SETTINGS_FILE_PATH.open('r', encoding='utf-8') as f:
        settings = json.load(f)

    if 'users' not in settings:
        settings['users'] = {
            'thb112259': 'steamok7416',
            'agt8729': 'Apk66433',
        }

    if 'mods' not in settings:
        settings['mods'] = {}

    with LAUNCHER_SETTINGS_FILE_PATH.open('w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)
except FileNotFoundError:
    message_dialog(
        PROMPT_TOOLKIT_DIALOG_TITLE,
        f'没有找到启动器配置文件, 请检查当前目录是否是游戏根目录\n{CWD}',
        '退出',
    )
    exit(1)

MODS_DIR_PATH.mkdir(parents=True, exist_ok=True)
MOD_BOOT_FILES_PATH.mkdir(parents=True, exist_ok=True)
