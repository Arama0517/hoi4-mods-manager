import winreg
from pathlib import Path

with winreg.OpenKey(
    winreg.HKEY_CURRENT_USER,
    r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders',
) as key:
    _DOCUMENTS_DIR_PATH, _ = winreg.QueryValueEx(key, 'Personal')

CWD = Path.cwd()
DATA_DIR_PATH = Path(_DOCUMENTS_DIR_PATH) / 'Paradox Interactive' / 'Hearts of Iron IV'

MODS_DIR_PATH = CWD / 'mods'
MOD_BOOT_FILES_PATH = DATA_DIR_PATH / 'mod'

# 启动器配置文件
LAUNCHER_SETTINGS_FILE_PATH = CWD / 'launcher-settings.json'
