from pathlib import Path

import tomli
from lib_not_dr.nuitka import nuitka_config_type, raw_config_type


def main(raw_config: raw_config_type) -> nuitka_config_type:
    config: nuitka_config_type = raw_config['cli']  # type: ignore
    with (Path().cwd() / 'pyproject.toml').open('rb') as f:
        version = tomli.load(f)['project']['version']
        config['product-version'] = version
        config['file-version'] = version
    return config
