import json
import shutil

from prompt_toolkit.shortcuts import checkboxlist_dialog, message_dialog

from src.common import settings
from src.common.cmd import clear
from src.common.dialog import PROMPT_TOOLKIT_DIALOG_TITLE
from src.common.path import LAUNCHER_SETTINGS_FILE_PATH, MOD_BOOT_FILES_PATH, MODS_DIR_PATH


def main():
    clear()

    options: list[tuple[str, str]] = []
    for item_id, item_info in settings['mods'].items():
        options.append((item_id, item_info['title']))
    if not options:
        message_dialog(PROMPT_TOOLKIT_DIALOG_TITLE, '你还没有安装任何模组', '返回').run()
        return

    items_id = checkboxlist_dialog(
        PROMPT_TOOLKIT_DIALOG_TITLE, '请选择要卸载的模组', '卸载', '取消', options
    ).run()
    if not items_id:
        return

    for item_id in items_id:
        shutil.rmtree(MODS_DIR_PATH / item_id)
        del settings['mods'][item_id]
        (MOD_BOOT_FILES_PATH / f'{item_id}.mod').unlink(missing_ok=True)

    with LAUNCHER_SETTINGS_FILE_PATH.open('w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)
    message_dialog(PROMPT_TOOLKIT_DIALOG_TITLE, '卸载完成', '返回').run()
