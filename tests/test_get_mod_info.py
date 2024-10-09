from steam import webapi
from steam.enums import EResult


def test_get_mod_info():
    items_id = ['820260968']
    result = webapi.post(
        'ISteamRemoteStorage',
        'GetPublishedFileDetails',
        params={'itemcount': len(items_id), 'publishedfileids': items_id},
    )

    assert EResult(result['response']['result']) == EResult.OK
