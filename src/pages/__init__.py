from .install import main as install
from .settings import main as settings
from .start import main as start
from .uninstall import main as uninstall
from .update import main as update

__all__ = ['install', 'start', 'uninstall', 'update', 'settings']
