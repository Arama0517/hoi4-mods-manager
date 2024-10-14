import sys

import requests
from loguru import logger
from prompt_toolkit.shortcuts import message_dialog, radiolist_dialog, yes_no_dialog
from rich import get_console
from rich.logging import RichHandler
from rich.traceback import Traceback
from steam import webapi
from steam.client import SteamClient
from steam.client.cdn import CDNClient
from steam.enums import EResult
from steam.webauth import WebAuth

from src.common import settings
from src.common.cmd import clear
from src.common.dialog import PROMPT_TOOLKIT_DIALOG_TITLE
from src.hoi4_mods_manager import install, start, uninstall, update

while True:
    try:
        webapi.get('ISteamWebAPIUtil', 'GetServerInfo')
        break
    except requests.exceptions.SSLError:
        if yes_no_dialog(
            PROMPT_TOOLKIT_DIALOG_TITLE,
            'SSL错误, 请关闭类似Watt toolkit的加速Steam功能后点击确认',
            '确认',
            '退出',
        ).run():
            continue
        else:
            sys.exit(1)

options = [
    ('start', '启动客户端'),
]

steam_client = SteamClient()

webauth = WebAuth()
for user, password in settings['users'].items():
    logger.info(f'尝试登录: {user}')
    webauth.cli_login(user, password)
    match steam_client.login(webauth.username, access_token=webauth.refresh_token):
        case EResult.OK:
            logger.info('成功')
            break
        case EResult.AlreadyLoggedInElsewhere:
            logger.warning('已在其他地方登录')
        case _ as e:
            logger.error(f'登录失败, 错误: {e.name}, 错误代码: {e.value}')
    webauth.logout_everywhere()
    steam_client.logout()

if not steam_client.logged_on:
    message_dialog('没有可用的账号, 无法使用模组相关功能')
else:
    options += [
        ('install', '安装模组'),
        ('uninstall', '卸载模组'),
        ('update', '更新模组'),
    ]

steam_cdn_client = CDNClient(steam_client)


if __name__ == '__main__':
    # 不知道为什么nuitka编译后会导致excepthook失效, 似乎是nuitka自己的问题
    def excepthook(exc_type, exc_value, traceback):
        from src.common.cmd import pause

        get_console().print(
            Traceback.from_exception(exc_type, exc_value, traceback, show_locals=True)
        )
        pause()

    sys.excepthook = excepthook

    logger.remove()
    logger.add(RichHandler(rich_tracebacks=True))

    while True:
        clear()
        result = radiolist_dialog(
            PROMPT_TOOLKIT_DIALOG_TITLE, '请选择一个选项', '确定', '退出', options
        ).run()
        match result:
            case None:
                sys.exit(0)
            case 'start':
                start.main()
                sys.exit(0)
            case 'install':
                install.main(steam_cdn_client)
            case 'uninstall':
                uninstall.main()
            case 'update':
                update.main(steam_cdn_client)
