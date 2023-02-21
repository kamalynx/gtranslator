# Класс для работы с Google Translate API в виде контекстного менеджера

С помощью этого модуля, можно переводить текст с одного языка на другой при помощи Google Translate.
Используется как контекстный менеджер Python.


## Установка

В качестве пакетного менеджера используется Poetry

`poetry install`


## Пример использования

```python
import asyncio
from translator import Translate


async def main():
	async with Translate(source_lang='en', target_lang='ru') as translator:
		result = await translator.translate('Hello World')

	return result


asyncio.run(main())
```

Переданная функции translate строка может быть как обычной, так и содержащей html разметку, которая будет удалена при помощи markupsafe.
