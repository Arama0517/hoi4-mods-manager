from lib_not_dr.nuitka import nuitka_config_type, raw_config_type

from src.version import BUILD_VERSION, VERSION


def main(raw_config: raw_config_type) -> nuitka_config_type:
    config: nuitka_config_type = raw_config['cli']  # type: ignore

    config['product-version'] = VERSION
    config['file-version'] = BUILD_VERSION

    return config
