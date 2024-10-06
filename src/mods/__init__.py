import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from rich.progress import Progress
from steam.client.cdn import CDNDepotFile, CDNDepotManifest, ManifestError

from utils import (
    LAUNCHER_SETTINGS as LAUNCHER_SETTINGS,
    LAUNCHER_SETTINGS_FILE_PATH as LAUNCHER_SETTINGS_FILE_PATH,
    MODS_DIR_PATH,
    STEAM_CDN_CLIENT,
    TITLE as TITLE,
    message_dialog as message_dialog,
)


def _write_mod_data(files: list[CDNDepotFile], mod_dir_path: Path, progress: Progress):
    task_id = progress.add_task('', total=len(files))
    for file in files:
        if file.is_directory:
            progress.update(task_id, advance=1)
            continue
        path: Path = mod_dir_path / file.filename
        description = (
            f'[bold green]线程 [bold red]{task_id} [bold green]正在下载 [bold blue]{path.name}'
        )
        progress.update(task_id, description=description)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(file.read())
        progress.update(task_id, advance=1)
    progress.remove_task(task_id)


def download(item_id: str):
    result = STEAM_CDN_CLIENT.get_manifest_for_workshop_item(int(item_id))
    if isinstance(result, ManifestError):
        raise result
    result: CDNDepotManifest
    mod_dir_path = MODS_DIR_PATH / item_id
    files: list[CDNDepotFile] = list(result.iter_files())

    default_max_workers = os.cpu_count() * 2
    max_workers = len(files) if len(files) < default_max_workers else default_max_workers
    chunk_size = len(files) // max_workers
    with Progress() as progress:
        chunks: list[list[CDNDepotFile]] = []
        for i in range(max_workers):
            start_index = i * chunk_size
            end_index = start_index + chunk_size if i < max_workers - 1 else len(files)
            chunk = files[start_index:end_index]
            chunks.append(chunk)

        # 多线程下载
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for chunk in chunks:
                executor.submit(
                    _write_mod_data,
                    chunk,
                    mod_dir_path,
                    progress,
                )
