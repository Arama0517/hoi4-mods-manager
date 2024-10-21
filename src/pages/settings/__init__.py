from prompt_toolkit.shortcuts import radiolist_dialog
from steam.client import SteamClient

from src.dialog import PROMPT_TOOLKIT_DIALOG_TITLE
from src.pages.settings.download_max_threads import download_max_threads
from src.pages.settings.max_chunk_size import max_chunk_size
from src.pages.settings.users import users

__all__ = ['main']


def main(steam_client: SteamClient):
    options = [
        ('users', 'steam账号'),
        ('download_threads', '下载时使用线程的最大数量'),
        ('max_chunk_size', '下载时切片的大小(仅适用于超过1M的大文件)'),
    ]
    while True:
        match radiolist_dialog(
            PROMPT_TOOLKIT_DIALOG_TITLE, '请选择要配置的选项', '确认', '返回', options
        ).run():
            case 'users':
                users(steam_client)
            case 'download_threads':
                download_max_threads()
            case 'max_chunk_size':
                max_chunk_size()
            case _:
                return
