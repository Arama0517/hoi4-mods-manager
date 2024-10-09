import json

from steam.client import SteamClient, SteamError
from steam.enums import EResult

from src.common.path import LAUNCHER_SETTINGS_FILE_PATH


def get_steam_client() -> SteamClient:
    with LAUNCHER_SETTINGS_FILE_PATH.open() as f:
        settings = json.load(f)

    client = SteamClient()
    for user, password in settings['users'].items():
        result = client.cli_login(user, password)
        match result:
            case EResult.OK:
                break
            case EResult.AlreadyLoggedInElsewhere:
                continue
            case _:
                raise SteamError('登录失败', result)
    if not client.logged_on:
        raise SteamError('登录失败')
    return client
