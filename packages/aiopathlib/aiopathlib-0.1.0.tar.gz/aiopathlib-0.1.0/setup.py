# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['aiopathlib']
install_requires = \
['aiofiles>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'aiopathlib',
    'version': '0.1.0',
    'description': 'Pathlib support for asyncio',
    'long_description': "aiopathlib: Pathlib support for asyncio\n==================================\n\n**aiopathlib** is written in Python, for handling local\ndisk files in asyncio applications.\n\nBase on `aiofiles` and just like pathlib, but use await.\n\n.. code-block:: python\n\n    with open('filename', 'w') as f:\n        f.write('My file contents')\n\n    text = await aiopathlib.AsyncPath('filename').read_text()\n    print(text)\n    'My file contents'\n\n    content = await aiopathlib.AsyncPath(Path('filename')).read_bytes()\n    print(cotent)\n    b'My file contents'\n\n\nAsynchronous interface to create folder.\n\n.. code-block:: python\n\n    await AsyncPath('dirname').mkdir(parents=True)\n\n\nFeatures\n--------\n\n- a file API very similar to Python's standard package `pathlib`, blocking API\n- support for buffered and unbuffered binary files, and buffered text files\n- support for ``async``/``await`` (:PEP:`492`) constructs\n\n\nInstallation\n------------\n\nTo install aiofiles, simply:\n\n.. code-block:: bash\n\n    $ pip install git+https://gitee.com/waketzheng/aiopathlib.git\n\n\nUsage\n-----\n\n\n* ``read_text``\n* ``read_bytes``\n* ``read_json``\n* ``write_text``\n* ``write_bytes``\n* ``write_json``\n* ``mkdir``\n* ``exists``\n* ``rename``\n* ``remove``\n\n\nHistory\n~~~~~~~\n\n0.1.0 (2021-06-13)\n``````````````````\n\n- Introduced a changelog.\n- Publish at gitee.\n\n\nContributing\n~~~~~~~~~~~~\nContributions are very welcome.\n",
    'author': 'Waket Zheng',
    'author_email': 'waketzheng@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/waketzheng/aiopathlib',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
