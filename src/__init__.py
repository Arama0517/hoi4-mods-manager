import warnings

import urllib3


def init():
    import requests
    from loguru import logger
    from rich.logging import RichHandler

    from src.settings import settings

    # 设置 logger
    logger.remove()
    logger.add(RichHandler())

    # 适配用反代加速Steam的工具
    origin = requests.Session.__init__

    def patched(self):
        origin(self)
        self.verify = settings.get('ssl') or True

    warnings.filterwarnings('ignore', category=urllib3.exceptions.InsecureRequestWarning)

    requests.Session.__init__ = patched


init()
