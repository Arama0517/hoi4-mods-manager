from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterator

from rich.progress import (
    BarColumn,
    Progress,
    ProgressColumn,
    TaskID,
    TextColumn,
)
from steam.client.cdn import CDNClient, CDNDepotFile, CDNDepotManifest

from src.path import MODS_DIR_PATH
from src.settings import settings

__all__ = ['download']


def _format_size(size: int):
    units = ['B', 'KiB', 'MiB', 'GiB', 'TiB']
    size = size
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f'{size:.2f} {units[unit_index]}'


def _write_mod_files(
    files: Iterator[CDNDepotFile],
    download_path: Path,
    progress: Progress,
    task_id: TaskID,
):
    for file in files:
        file_path: Path = download_path / file.filename
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # 分片写入
        with file_path.open('wb') as f:
            if file.size >= 1048576:
                while True:
                    data: bytes = file.read(settings['max_chunk_size'])
                    if not data:
                        break
                    f.write(data)
                    progress.advance(task_id, len(data))
            else:
                f.write(file.read())
                progress.advance(task_id, file.size)


def _sort_cdn_depot_files(
    manifest: CDNDepotManifest,
) -> tuple[Iterator[Iterator[CDNDepotFile]], int]:
    files = [target for target in manifest.iter_files() if not target.is_directory]

    max_chunks = min(len(files), settings['download_max_threads'])
    chunks = [[] for _ in range(max_chunks)]
    chunk_sizes = [0] * max_chunks

    min_chunk_index = 0

    for file in sorted(files, key=lambda f: f.size, reverse=True):
        chunks[min_chunk_index].append(file)
        chunk_sizes[min_chunk_index] += file.size

        min_size = chunk_sizes[min_chunk_index]
        for i in range(max_chunks):
            if chunk_sizes[i] < min_size:
                min_chunk_index = i
                min_size = chunk_sizes[i]

    total_size = sum(chunk_sizes)

    return (iter(chunk) for chunk in chunks), total_size


class FileSizeProgressColumn(ProgressColumn):
    total: str = ''

    def __init__(self):
        super().__init__()

    def render(self, task):
        if not self.total:
            self.total = _format_size(int(task.total))
        if task.finished:
            return ''
        return f'[red]{_format_size(int(task.completed))} [bold dim]/ [green]{self.total}'


def download(item_id: str, steam_cdn_client: CDNClient) -> timedelta:
    manifest = steam_cdn_client.get_manifest_for_workshop_item(int(item_id))
    if isinstance(manifest, Exception):
        raise manifest
    download_path = MODS_DIR_PATH / item_id
    start_time = datetime.now()
    with Progress(
        TextColumn('[progress.description]{task.description}'),
        BarColumn(),
        # TaskProgressColumn(),
        FileSizeProgressColumn(),
    ) as progress:
        chunks, files_size = _sort_cdn_depot_files(manifest)
        task_id = progress.add_task('[bold dim]正在下载模组中...', total=files_size)
        with ThreadPoolExecutor(max_workers=settings['download_max_threads']) as executor:
            for chunk in chunks:
                executor.submit(_write_mod_files, chunk, download_path, progress, task_id)
    return datetime.now() - start_time
