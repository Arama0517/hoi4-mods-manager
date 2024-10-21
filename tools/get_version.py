from pathlib import Path

import tomli

with (Path().cwd() / 'pyproject.toml').open('rb') as f:
    print(tomli.load(f)['project']['version'])
