import time

from loguru import logger
from prompt_toolkit.shortcuts import message_dialog

import mods
from utils import LAUNCHER_SETTINGS, MOD_BOOT_FILES_PATH, STEAM_WEBAPI, TITLE


def main():
    items_id = list(LAUNCHER_SETTINGS['mods'].keys())
    if len(items_id) == 0:
        message_dialog(TITLE, '你还没有安装任何模组', '返回').run()
        return
    items_info = STEAM_WEBAPI.call(
        'ISteamRemoteStorage.GetPublishedFileDetails',
        itemcount=1,
        publishedfileids=items_id,
    )['response']['publishedfiledetails']
    for item_info in items_info:
        item_id = item_info['publishedfileid']
        if item_info['time_updated'] != LAUNCHER_SETTINGS['mods'][item_id]['time_updated']:
            mods.download(item_info)
            LAUNCHER_SETTINGS['mods'][item_id] = item_info
            (MOD_BOOT_FILES_PATH / f'{item_id}.mod').unlink(missing_ok=True)
        else:
            logger.info(f'{item_info['title']} 已经是最新版本')
    time.sleep(1)
    message_dialog(TITLE, '更新完成', '返回').run()
