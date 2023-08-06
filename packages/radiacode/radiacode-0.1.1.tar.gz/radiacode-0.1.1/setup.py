# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['radiacode', 'radiacode.decoders', 'radiacode.transports']

package_data = \
{'': ['*']}

install_requires = \
['bluepy>=1.3.0,<2.0.0', 'pyusb>=1.1.1,<2.0.0']

extras_require = \
{'examples': ['aiohttp>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'radiacode',
    'version': '0.1.1',
    'description': 'Library for RadiaCode-101',
    'long_description': "## RadiaCode\nБиблиотека для работы с дозиметром [RadiaCode-101](https://scan-electronics.com/dosimeters/radiacode/radiacode-101), находится в разработке - API не стабилен и возможны изменения.\n\nПример использования ([backend](radiacode-examples/webserver.py), [frontend](radiacode-examples/webserver.html)):\n![radiacode-webserver-example](./screenshot.png)\n\n### Установка & запуск примера\n```\n# установка вместе с зависимостями для примеров, уберите [examples] если они вам не нужны\n$ pip3 install 'radiacode[examples]' --upgrade\n\n# Запуск вебсервера из скриншота выше\n# bluetooth: замените на адрес вашего устройства\n$ python3 -m radiacode-examples.webserver --bluetooth-mac 52:43:01:02:03:04\n\n# или то же самое, но по usb\n$ sudo python3 -m radiacode-examples.webserver\n\n# или простой пример с выводом информации в терминал, опции аналогичны webserver\n$ python3 -m radiacode-examples.basic\n```\n\n### Разработка\n- Установить [python poetry](https://python-poetry.org/docs/#installation)\n- Склонировать репозиторий, установить и запустить:\n```\n$ git clone https://github.com/cdump/radiacode.git\n$ cd radiacode\n$ poetry install\n$ poetry run python3 radiacode-examples/basic.py --bluetooth-mac 52:43:01:02:03:04  # или без --bluetooth-mac для USB подключения\n```\n",
    'author': 'Maxim Andreev',
    'author_email': 'andreevmaxim@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cdump/radiacode',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
