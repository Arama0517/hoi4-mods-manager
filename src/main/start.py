import re
import subprocess
from pathlib import Path

from loguru import logger

from utils import CWD, MOD_BOOT_FILES_PATH, MODS_DIR_PATH


def main():
    for file in MOD_BOOT_FILES_PATH.iterdir():
        if file.suffix != '.mod':
            continue
        with file.open('r', encoding='utf-8') as f:
            data = f.read()
        result = re.search(r'(?:^|[^a-zA-Z_])path\s*=\s*"([^"]+)"', data, flags=0)

        # 没有找到path字段
        if not result:
            logger.info(f'删除无效定位文件: {file}')
            file.unlink()
            continue

        mod_path = Path(result.group(1))
        # mod源目录不存在
        if not mod_path.exists():
            logger.info(f'删除无效定位文件: {file}')
            file.unlink()
            continue

    # 生成mod定位文件
    for mod in MODS_DIR_PATH.iterdir():
        mod_boot_file_path = MOD_BOOT_FILES_PATH / f'{mod.name}.mod'
        ok = False
        for f in mod.iterdir():
            if f.suffix == '.mod':
                ok = True
                mod_decsriptor_file_path = f
                break

        # 没有找到描述文件, 可能不是mod; 跳过
        if not ok:
            continue

        if not mod_boot_file_path.exists():
            with mod_boot_file_path.open('w', encoding='utf-8') as f:
                f.write(mod_decsriptor_file_path.read_text(encoding='utf-8'))
                f.write(f'\npath="{mod.as_posix()}"')

    subprocess.run(CWD / 'dowser.exe', cwd=CWD)
