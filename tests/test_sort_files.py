from rich import print

from src.common import mods
from src.hoi4_mods_manager.main import steam_cdn_client


def test_sort_files():
    manifest = steam_cdn_client.get_manifest_for_workshop_item(3292237090)
    if isinstance(manifest, Exception):
        raise manifest
    chunks = mods._sort_cdn_depot_files(manifest)
    for chunk in chunks:
        print(len(chunk))


if __name__ == '__main__':
    test_sort_files()
