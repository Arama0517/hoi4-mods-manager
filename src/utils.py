import json
import logging
import subprocess
import sys
import winreg
from pathlib import Path

from loguru import logger
from prompt_toolkit.shortcuts import message_dialog
from rich.logging import RichHandler
from steam.client import SteamClient
from steam.client.cdn import CDNClient
from steam.enums import EResult
from steam.webapi import DEFAULT_PARAMS, WebAPI


# 常用函数
def pause() -> None:
    subprocess.run(['cmd', '/c', 'pause'])


def clear() -> None:
    subprocess.run(['cmd', '/c', 'cls'])


# log
logger.remove()
logger.add(RichHandler(logging.DEBUG))

# dialog
TITLE = '钢铁雄心4模组管理器'

# 文档目录
with winreg.OpenKey(
    winreg.HKEY_CURRENT_USER,
    r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders',
) as key:
    _DOCUMENTS_DIR_PATH, _ = winreg.QueryValueEx(key, 'Personal')

# 路径
CWD = Path.cwd()
DATA_DIR_PATH = Path(_DOCUMENTS_DIR_PATH) / 'Paradox Interactive' / 'Hearts of Iron IV'

MODS_DIR_PATH = CWD / 'mods'
MOD_BOOT_FILES_PATH = DATA_DIR_PATH / 'mod'


# STEAMCMD_DIR_PATH = CWD / 'steamcmd'
# STEAMCMD_EXE_PATH = STEAMCMD_DIR_PATH / 'steamcmd.exe'
# STEAMCMD_CONTENTS_DIR_PATH = STEAMCMD_DIR_PATH / 'steamapps' / 'workshop' / 'content' / '394360'
# STEAMCMD_ITEMS_INFO_FILE_PATH = (
#     STEAMCMD_DIR_PATH / 'steamapps' / 'workshop' / 'appworkshop_394360.acf'
# )

# 创建文件夹
MODS_DIR_PATH.mkdir(parents=True, exist_ok=True)
MOD_BOOT_FILES_PATH.mkdir(parents=True, exist_ok=True)

# 启动器配置文件
LAUNCHER_SETTINGS_FILE_PATH = CWD / 'launcher-settings.json'

# 检查启动器配置文件是否存在
if not LAUNCHER_SETTINGS_FILE_PATH.exists():
    logger.critical('启动器配置文件不存在, 请检查当前目录下是否是游戏根目录!')
    pause()
    sys.exit(1)

with LAUNCHER_SETTINGS_FILE_PATH.open('r', encoding='utf-8') as f:
    LAUNCHER_SETTINGS = json.load(f)

if 'mods' not in LAUNCHER_SETTINGS:
    LAUNCHER_SETTINGS['mods'] = {}

if 'users' not in LAUNCHER_SETTINGS:
    LAUNCHER_SETTINGS['users'] = {'thb112259': 'steamok7416', 'agt8729': 'Apk66433'}

with LAUNCHER_SETTINGS_FILE_PATH.open('w', encoding='utf-8') as f:
    json.dump(LAUNCHER_SETTINGS, f, indent=4, ensure_ascii=False)

# Steam
STEAM_WEBAPI = WebAPI(DEFAULT_PARAMS['key'])
STEAM_CLIENT = SteamClient()
for user, password in LAUNCHER_SETTINGS['users'].items():
    result = STEAM_CLIENT.cli_login(user, password)
    if result == EResult.OK:
        break
if not STEAM_CLIENT.logged_on:
    message_dialog(title=TITLE, text='暂时没有可用的账号, 无法使用模组相关功能').run()
STEAM_CDN_CLIENT = CDNClient(STEAM_CLIENT)
