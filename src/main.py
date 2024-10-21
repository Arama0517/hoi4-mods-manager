import atexit
import sys
import traceback

import requests
from loguru import logger
from prompt_toolkit.shortcuts import message_dialog, radiolist_dialog, yes_no_dialog
from rich.logging import RichHandler
from steam import webapi

from src import pages
from src.dialog import PROMPT_TOOLKIT_DIALOG_TITLE
from src.path import DATA_DIR_PATH, LAUNCHER_SETTINGS_FILE_PATH, MOD_BOOT_FILES_PATH, MODS_DIR_PATH
from src.settings import save_settings, settings

logger.remove()
logger.add(RichHandler(rich_tracebacks=True))

while True:
    try:
        webapi.get('ISteamWebAPIUtil', 'GetServerInfo')
        break
    except requests.exceptions.SSLError:
        if yes_no_dialog(
            PROMPT_TOOLKIT_DIALOG_TITLE,
            'SSL错误\n请关闭类似Watt toolkit的加速Steam功能后点击确认',
            '确认',
            '退出',
        ).run():
            continue
        else:
            sys.exit(1)


def main():
    def except_hook(exc_type, exc_value, exc_traceback):
        message_dialog(
            PROMPT_TOOLKIT_DIALOG_TITLE,
            f"""发生了一个错误:
{''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))}""",
            '退出',
        ).run()

    sys.excepthook = except_hook

    def exit_hook():
        if client.logged_on:
            logger.info('登出')
            client.logout()

    atexit.register(exit_hook)

    if not LAUNCHER_SETTINGS_FILE_PATH.exists():
        message_dialog(
            PROMPT_TOOLKIT_DIALOG_TITLE,
            '没有找到启动器配置文件, 请检查当前目录是否正确',
            '退出',
        ).run()
        return 1

    # 修改存放数据的目录
    settings['gameDataPath'] = str(DATA_DIR_PATH)
    save_settings()

    MODS_DIR_PATH.mkdir(parents=True, exist_ok=True)
    MOD_BOOT_FILES_PATH.mkdir(parents=True, exist_ok=True)

    while True:
        options = [
            ('start', '启动客户端'),
        ]
        text = '请选择一个选项'
        if not client.logged_on:
            text += '\n没有可用的账号, 无法使用模组相关功能'
        else:
            options += [
                ('install', '安装模组'),
                ('uninstall', '卸载模组'),
                ('update', '更新模组'),
            ]
        options += [('settings', '设置')]

        match radiolist_dialog(PROMPT_TOOLKIT_DIALOG_TITLE, text, '确定', '退出', options).run():
            case 'start':
                pages.start()
                break
            case 'install':
                pages.install(cdn_client)
            case 'uninstall':
                pages.uninstall()
            case 'update':
                pages.update(cdn_client)
            case 'settings':
                pages.settings(client)
            case _:
                break


if __name__ == '__main__':
    from src.steam_clients import cdn_client, client

    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
