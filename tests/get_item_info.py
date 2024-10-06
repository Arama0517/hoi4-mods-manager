import json
from sys import argv

from src.utils import STEAM_WEBAPI

if __name__ == '__main__':
    items_id = argv[1:]
    result = STEAM_WEBAPI.call(
        'ISteamRemoteStorage.GetPublishedFileDetails',
        itemcount=len(items_id),
        publishedfileids=items_id,
    )
    print(json.dumps(result, indent=4, ensure_ascii=False))
