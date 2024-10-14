import subprocess

from rich import print


def clear() -> None:
    subprocess.run(['cmd', '/c', 'cls'])


def pause() -> None:
    print('[bold blue]请按任意键继续...')
    subprocess.run(['cmd', '/c', 'pause'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
