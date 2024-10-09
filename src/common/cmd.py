import subprocess


def clear() -> None:
    subprocess.run(['cmd', '/c', 'cls'])


def pause() -> None:
    subprocess.run(['cmd', '/c', 'pause'])
