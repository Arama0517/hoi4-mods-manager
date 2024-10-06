import json
import shutil

from prompt_toolkit.shortcuts import checkboxlist_dialog, message_dialog

from utils import (
    LAUNCHER_SETTINGS,
    LAUNCHER_SETTINGS_FILE_PATH,
    MOD_BOOT_FILES_PATH,
    MODS_DIR_PATH,
    TITLE,
    clear,
)


def main():
    clear()
    options: list[tuple[str, str]] = []
    for item_id, item_info in LAUNCHER_SETTINGS['mods'].items():
        options.append((item_id, item_info['title']))
    if not options:
        message_dialog(TITLE, '你还没有安装任何模组', '返回').run()
        return
    items_id = checkboxlist_dialog(TITLE, '请选择要卸载的模组', '卸载', '取消', options).run()
    print(items_id)
    if not items_id:
        return
    for item_id in items_id:
        shutil.rmtree(MODS_DIR_PATH / item_id)
        del LAUNCHER_SETTINGS['mods'][item_id]
        (MOD_BOOT_FILES_PATH / f'{item_id}.mod').unlink(missing_ok=True)
    with LAUNCHER_SETTINGS_FILE_PATH.open('w', encoding='utf-8') as f:
        json.dump(LAUNCHER_SETTINGS, f, indent=4, ensure_ascii=False)
    message_dialog(TITLE, '卸载完成', '返回').run()
