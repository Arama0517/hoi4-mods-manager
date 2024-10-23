import atexit
import sys
import traceback

import requests
from loguru import logger
from prompt_toolkit.shortcuts import input_dialog, message_dialog, radiolist_dialog
from steam import webapi
from steam.webauth import WebAuth, WebAuthException

from src import pages
from src.dialog import PROMPT_TOOLKIT_DIALOG_TITLE
from src.pages.settings.certificate import CertificatePathValidator
from src.path import DATA_DIR_PATH, LAUNCHER_SETTINGS_FILE_PATH, MOD_BOOT_FILES_PATH, MODS_DIR_PATH
from src.settings import DEFAULT_USERS, save_settings, settings

# 检测SSL错误
while True:
    try:
        webapi.get('ISteamWebAPIUtil', 'GetServerInfo')
        break
    except requests.exceptions.SSLError:
        ssl = radiolist_dialog(
            PROMPT_TOOLKIT_DIALOG_TITLE,
            'SSL错误\n请选择一个选项',
            '确认',
            '退出',
            [
                ('retry', '重试'),
                ('disable_ssl', '关闭证书认证'),
                ('set_local_certificate', '设置本地证书路径'),
            ],
        ).run()
        match ssl:
            case None:
                sys.exit(1)
            case 'retry':
                continue
            case 'disable_ssl':
                settings['ssl'] = False
            case 'set_local_certificate':
                certificate_path = input_dialog(
                    PROMPT_TOOLKIT_DIALOG_TITLE,
                    '请输入证书路径',
                    validator=CertificatePathValidator(),
                ).run()
                settings['ssl'] = certificate_path
        save_settings()


for user_name, password in DEFAULT_USERS.items():
    webauth = WebAuth()
    try:
        webauth.login(user_name, password)
    except WebAuthException:
        continue
    if not webauth.logged_on:
        continue
    settings['users'][user_name] = {
        'user_name': user_name,
        'password': password,
        'token': webauth.refresh_token,
    }
save_settings()


def main():
    from src.steam_clients import cdn_client, client

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
        text = '请选择一个选项'
        options = [
            ('start', '启动客户端'),
        ]
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
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
