from prompt_toolkit.document import Document
from prompt_toolkit.shortcuts import input_dialog
from prompt_toolkit.validation import ValidationError, Validator

from src.dialog import PROMPT_TOOLKIT_DIALOG_TITLE
from src.settings import save_settings, settings

__all__ = ['max_chunk_size']


class _MaxChunkSizeValidator(Validator):
    def validate(self, document: Document) -> None:
        if not document.text:
            raise ValidationError(message='不能为空')
        if not document.text.isdigit() and int(document.text) <= 0:
            raise ValidationError(message='请输入一个有效的数字')


def max_chunk_size():
    _max_chunk_size = input_dialog(
        PROMPT_TOOLKIT_DIALOG_TITLE,
        """请输入要设置的大小, 单位为字节
不会对下载小文件(<1M)有任何帮助, 并且会导致下载大文件时占用内存大""",
        '确认',
        '返回',
        validator=_MaxChunkSizeValidator(),
        default=settings['max_chunk_size'],
    ).run()
    if not _max_chunk_size and _max_chunk_size == settings['max_chunk_size']:
        return
    settings['max_chunk_size'] = _max_chunk_size
    save_settings()
