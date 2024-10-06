import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from rich.progress import (
    BarColumn,
    Progress,
    TaskID,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)
from steam.client.cdn import CDNDepotFile, CDNDepotManifest, ManifestError

from utils import (
    LAUNCHER_SETTINGS as LAUNCHER_SETTINGS,
    LAUNCHER_SETTINGS_FILE_PATH as LAUNCHER_SETTINGS_FILE_PATH,
    MODS_DIR_PATH,
    STEAM_CDN_CLIENT,
    TITLE as TITLE,
    message_dialog as message_dialog,
)


def _write_mod_data(
    files: list[CDNDepotFile], mod_dir_path: Path, task_id: TaskID, progress: Progress
):
    for file in files:
        if file.is_directory:
            continue
        path: Path = mod_dir_path / file.filename
        progress.update(task_id, file_name=path.name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(file.read())
        progress.update(task_id, advance=1)


def download(item_id: str):
    result: ManifestError | CDNDepotManifest = STEAM_CDN_CLIENT.get_manifest_for_workshop_item(
        int(item_id)
    )
    if isinstance(result, ManifestError):
        raise result
    result: CDNDepotManifest
    mod_dir_path = MODS_DIR_PATH / item_id
    files: list[CDNDepotFile] = list(result.iter_files())

    default_max_workers = os.cpu_count() * 2
    max_workers = len(files) if len(files) < default_max_workers else default_max_workers
    chunk_size = len(files) // max_workers
    with Progress(
        TextColumn('[bold green]{task.description}'),
        TextColumn('[bold blue]{task.fields[file_name]}'),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
    ) as progress:
        chunks = []
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
                    progress.add_task('正在下载', total=len(chunk), file_name=''),
                    progress,
                )
