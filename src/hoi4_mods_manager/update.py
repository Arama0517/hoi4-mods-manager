import time

from loguru import logger
from prompt_toolkit.shortcuts import message_dialog
from steam import webapi
from steam.client.cdn import CDNClient

from src.common import mods, settings
from src.common.dialog import PROMPT_TOOLKIT_DIALOG_TITLE
from src.common.path import MOD_BOOT_FILES_PATH


def main(cdn_client: CDNClient):
    items_id = list(settings['mods'].keys())
    if len(items_id) == 0:
        message_dialog(PROMPT_TOOLKIT_DIALOG_TITLE, '你还没有安装任何模组', '返回').run()
        return
    items_info = webapi.post(
        'ISteamRemoteStorage',
        'GetPublishedFileDetails',
        params={
            'itemcount': len(items_id),
            'publishedfileids': items_id,
        },
    )['response']['publishedfiledetails']
    for item_info in items_info:
        item_id = item_info['publishedfileid']
        if item_info['time_updated'] != settings['mods'][item_id]['time_updated']:
            # 需要更新模组
            mods.download(item_info, cdn_client)
            settings['mods'][item_id] = item_info
            (MOD_BOOT_FILES_PATH / f'{item_id}.mod').unlink(missing_ok=True)
        else:
            logger.info(f'{item_info['title']} 已经是最新版本')
    time.sleep(1)
    message_dialog(PROMPT_TOOLKIT_DIALOG_TITLE, '更新完成', '返回').run()
