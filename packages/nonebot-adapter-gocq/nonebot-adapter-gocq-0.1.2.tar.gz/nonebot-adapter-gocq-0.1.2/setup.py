# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_adapter_gocq']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.17.0,<0.18.0', 'nonebot2==2.0.0-alpha.13']

setup_kwargs = {
    'name': 'nonebot-adapter-gocq',
    'version': '0.1.2',
    'description': 'go-cqhttp adapter for nonebot2',
    'long_description': '<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/nonebot2/master/docs/.vuepress/public/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n\n# NoneBot Adapter GOCQ\n\n_✨ go-cqhttp 协议适配 ✨_\n\n在原 CQHTTP Adapter 的基础上进行了修改以便于更好地适配 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)\n\n</div>\n\n## Guide\n\n[使用指南](./docs/manual.md)\n\n## Feature\n\n- [x] 兼容 go-cqhttp 与 Onebot 标准不同的 API、Event、CQCode\n- [x] Request 事件的 approve、adject 方法不再需要 bot 参数\n\n## Bug\n\n- [x] 由于 at 的 CQ 码增加了 name 字段导致群里被 at 的 bot 上报的 to_me 字段恒为 false\n- [x] 私聊消息遇到错误，没有字段 temp_source\n',
    'author': 'Jigsaw',
    'author_email': 'j1g5aw@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Jigsaw111/nonebot-adapter-gocq',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
