import logging

from loguru import logger
from rich.logging import RichHandler
from rich.traceback import install

from . import mods, path, steam
from .settings import settings


def _init():
    # 美化错误
    install(show_locals=True)

    # 设置日志样式
    logger.remove()
    logger.add(RichHandler(logging.DEBUG))


_init()

__all__ = [
    'path',
    'mods',
    'steam',
    'settings',
]
