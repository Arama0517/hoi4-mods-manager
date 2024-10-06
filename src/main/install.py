import json
import shutil

from prompt_toolkit.document import Document
from prompt_toolkit.shortcuts import input_dialog, message_dialog, yes_no_dialog
from prompt_toolkit.validation import ValidationError, Validator
from steam.enums import EResult

import mods
from utils import (
    LAUNCHER_SETTINGS,
    LAUNCHER_SETTINGS_FILE_PATH,
    MODS_DIR_PATH,
    STEAM_WEBAPI,
    TITLE,
    clear,
)


class _SteamIDValidator(Validator):
    def validate(self, document: Document) -> None:
        if not document.text:
            raise ValidationError(message='不能为空')
        if not document.text.isdigit():
            raise ValidationError(message='请输入一个有效的创意工坊ID')
        item_info = STEAM_WEBAPI.call(
            'ISteamRemoteStorage.GetPublishedFileDetails',
            itemcount=1,
            publishedfileids=[document.text],
        )['response']['publishedfiledetails'][0]
        if item_info['result'] != EResult.OK:
            raise ValidationError(message='请输入一个有效的创意工坊ID')
        if item_info['consumer_app_id'] != 394360:
            raise ValidationError(message='暂不支持其他游戏的模组')


def main() -> None:
    while True:
        clear()
        item_id = input_dialog(
            TITLE,
            '请输入要安装的Mod的创意工坊ID',
            '安装',
            '返回',
            validator=_SteamIDValidator(),
        ).run()
        if item_id is None:
            break
        if item_id in LAUNCHER_SETTINGS['mods']:
            message_dialog(TITLE, '该Mod已经安装过了', '继续').run()
            continue

        item_info = STEAM_WEBAPI.call(
            'ISteamRemoteStorage.GetPublishedFileDetails',
            itemcount=1,
            publishedfileids=[item_id],
        )['response']['publishedfiledetails'][0]
        if not yes_no_dialog(
            TITLE,
            f'是否安装名为 {item_info['title']} 的Mod?',
            yes_text='安装',
            no_text='取消',
        ).run():
            continue

        try:
            mods.download(item_id)

            LAUNCHER_SETTINGS['mods'][item_id] = item_info
            with LAUNCHER_SETTINGS_FILE_PATH.open('w', encoding='utf-8') as f:
                json.dump(LAUNCHER_SETTINGS, f, indent=4, ensure_ascii=False)

            message_dialog(TITLE, '下载完成', '继续').run()
        except Exception as e:
            message_dialog(TITLE, f'下载失败, 请稍后再试\n错误: {e}', '继续').run()
            shutil.rmtree(MODS_DIR_PATH / item_id, ignore_errors=True)
            continue
