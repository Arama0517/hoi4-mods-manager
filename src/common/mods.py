import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from rich.progress import Progress
from steam.client.cdn import CDNClient, CDNDepotFile, CDNDepotManifest

from src.common.path import MODS_DIR_PATH


def _write_mod_files(files: list[CDNDepotFile], mod_dir_path: Path, progress: Progress):
    task_id = progress.add_task('', total=len(files))
    for file in files:
        path: Path = mod_dir_path / file.filename
        progress.update(task_id, description=f'[bold green]正在下载 [bold blue]{path.name}')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(file.read())
        progress.update(task_id, advance=1)
    progress.remove_task(task_id)


def _sort_cdn_depot_files(
    manifest: CDNDepotManifest,
    mod_dir_path: Path,
) -> tuple[list[list[CDNDepotFile]], list[Path]]:
    directories = []
    files = []
    for target in manifest.iter_files():
        if target.is_directory:
            directories.append(mod_dir_path / target.filename)
        else:
            files.append(target)

    max_chunks = min(len(files), os.cpu_count())
    chunks = [[] for _ in range(max_chunks)]
    chunk_sizes = [0] * max_chunks

    for file in sorted(files, key=lambda f: f.size, reverse=True):
        min_chunk_index = chunk_sizes.index(min(chunk_sizes))
        chunks[min_chunk_index].append(file)
        chunk_sizes[min_chunk_index] += file.size

    return chunks, directories


def download(item_id: str, steam_cdn_client: CDNClient):
    manifest = steam_cdn_client.get_manifest_for_workshop_item(int(item_id))
    if isinstance(manifest, Exception):
        raise manifest
    manifest: CDNDepotManifest
    mod_dir_path = MODS_DIR_PATH / item_id
    chunks, directories = _sort_cdn_depot_files(manifest, mod_dir_path)
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    with Progress() as progress:
        with ThreadPoolExecutor(max_workers=len(chunks)) as executor:
            for chunk in chunks:
                executor.submit(_write_mod_files, chunk, mod_dir_path, progress)
