import asyncio
import json
import time
from typing import Self
import sys

import httpx
from markupsafe import Markup


class Translator:
    """Простой переводчик текста с помощью Google Translate."""

    def __init__(
        self: Self, source_lang: str = 'en', target_lang: str = 'ru'
    ) -> None:
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.query_params = {
            'client': 'gtx',  # client google translate extension
            'sl': source_lang,
            'tl': target_lang,
            'hl': 'ru',  # язык интерфейса
            'dt': 't',  # вернуть только переведённый текст
            'ie': 'UTF-8',  # входящая кодировка
            'oe': 'UTF-8',  # исходящая кодировка
            'dj': 1,  # вернуть как json
        }

    async def __aenter__(self: Self) -> Self:
        """Инициализируем контекстный менеджер."""

        self.client = httpx.AsyncClient(
            base_url='https://translate.googleapis.com',
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'AndroidTranslate/5.3.0.RC02.130475354-53000263 5.1 phone TRANSLATE_OPM5_TEST_1'
            },
        )
        return self

    async def __aexit__(self: Self, exc_type, exc_value, traceback) -> None:
        """Закрываем контекстный менеджер."""

        await self.client.aclose()

    async def translate_string(self: Self, text: str):
        """Переводим одну строку."""
        self.query_params['format'] = 'text'  # отбрасывает html
        self.query_params['q'] = Markup(text).striptags()

        request = await self.client.get(
            '/translate_a/single', params=self.query_params
        )

        if 'application/json' in request.headers.get('Content-Type'):
            data = request.json()
            sentences = [p.get('trans') for p in data.get('sentences')]

            return ''.join(sentences)

        return request.text


if __name__ == '__main__':
    async def main():
        async with Translator() as tr:
            print(await tr.translate_string('<h1>hello world</span>'))

    sys.exit(asyncio.run(main()))
