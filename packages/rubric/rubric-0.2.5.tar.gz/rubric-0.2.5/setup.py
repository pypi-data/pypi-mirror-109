# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rubric', 'rubric.files']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['rubric = rubric.rubric:cli_entrypoint']}

setup_kwargs = {
    'name': 'rubric',
    'version': '0.2.5',
    'description': 'Initialize your Python project with all the linting boilerplates you need',
    'long_description': '<div align="center">\n\n<h1>Rubric</h1>\n<strong>>> <i>Automate the boilerplate while initializing your Python project</i> <<</strong>\n\n&nbsp;\n\n</div>\n\n![img](https://images.unsplash.com/photo-1582184520153-cb662f665f11?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1850&q=80)\n\n## Preface\n\nRubric is an opinionated project initializer for Python. It assumes that you\'ll use:\n\n* [Black](https://github.com/psf/black) as the primary code formatter.\n* [Isort](https://github.com/PyCQA/isort) to sort the imports.\n* [Flake8](https://github.com/PyCQA/flake8) to ensure style guide conformance.\n* [Mypy](https://github.com/python/mypy) to check the type hints.\n* [Pip-tools](https://github.com/jazzband/pip-tools) to manage the dependencies.\n\nFollowing is a list of config files that Rubric is going to add to your directory:\n\n```\nroot\n├── .flake8                  # Config file for .flake8\n├── .gitignore               # Python specific .gitignore file\n├── makefile                 # Makefile containing the commands to lint your code\n├── mypy.ini                 # Config file for mypy type checker\n├── pyproject.toml           # Toml file to hold a few common config vars\n├── README.md                # A readme boilerplate\n├── requirements-dev.in      # File to specify the top level dev requirements\n├── requirements-dev.txt     # File to specify the dev requirements\n├── requirements.in          # File to specify the top level app requirements\n└── requirements.txt         # File to specify the pinned app requirements\n```\n\nThe files will contain minimal but sensible default configurations for the respective tools. You\'re free to change them as you like.\n\n## Installation\n\n* Rubric requires Python 3.7 and up.\n\n* Make a virtual environment in your project\'s root directory.\n\n* Activate the environment and run:\n\n    ```\n    pip install rubric\n    ```\n\n## Usage\n\n* To inspect all the CLI options, run:\n\n    ```\n    rubric --help\n    ```\n\n    You should see the following output:\n\n    ```\n    $ rubric\n\n           ___       __       _\n          / _ \\__ __/ /  ____(_)___\n         / , _/ // / _ \\/ __/ / __/\n        /_/|_|\\_,_/_.__/_/ /_/\\__/\n\n    usage: rubric [-h] [-l] [-d DIRNAME] [-o OVERWRITE [OVERWRITE ...]] [-v] [run]\n\n    Rubric -- Initialize your Python project ⚙️\n\n    positional arguments:\n    run                   run rubric & initialize the project scaffold\n\n    optional arguments:\n    -h, --help            show this help message and exit\n    -l, --list            list the config files that are about to be generated\n    -d DIRNAME, --dirname DIRNAME\n                            target directory name\n    -o OVERWRITE [OVERWRITE ...], --overwrite OVERWRITE [OVERWRITE ...]\n                            overwrite existing config files, allowed values are: all, .flake8,\n                            .gitignore, README.md, makefile, mypy.ini, pyproject.toml,\n                            requirements-dev.in, requirements-dev.txt, requirements.in,\n                            requirements.txt\n    -v, --version         display the version number\n\n    ```\n\n* Initialize a project with the following command:\n\n    ```\n    rubric run\n    ```\n\n    This will run the tool in a non-destructive way—that means it won\'t overwrite any of the configuration files that you might have in the directory.\n\n    If you want to overwrite any of the existing config files that you might have in the directory, then run:\n\n    ```\n    rubric run --overwrite filename1 filename2\n    ```\n\n    You can also point Rubric to a directory.\n\n    ```\n    rubric run --directory "some/custom/directory"\n    ```\n\n<div align="center">\n<i> ✨ 🍰 ✨ </i>\n</div>\n',
    'author': 'rednafi',
    'author_email': 'redowan.nafi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rednafi/rubric',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
