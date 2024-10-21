from pathlib import Path

import tomli

with (Path().cwd() / 'pyproject.toml').open('rb') as f:
    version = tomli.load(f)['project']['version']

print(f'v{version}')
