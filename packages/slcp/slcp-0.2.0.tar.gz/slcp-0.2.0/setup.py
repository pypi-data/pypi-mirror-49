# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['slcp']
entry_points = \
{'console_scripts': ['slcp = slcp:main']}

setup_kwargs = {
    'name': 'slcp',
    'version': '0.2.0',
    'description': 'Copy all files with given extensions from a directory and its subfolders to another directory.',
    'long_description': "# Selective Copy\n[![Python Version](https://img.shields.io/pypi/pyversions/slcp.svg)](https://www.python.org/downloads/release/python-370/)\n[![PyPi Version](https://img.shields.io/pypi/v/slcp.svg)](https://pypi.org/project/slcp/)\n[![License](https://img.shields.io/github/license/pltnk/selective_copy.svg)](https://choosealicense.com/licenses/mit/)\n[![Codacy Badge](https://api.codacy.com/project/badge/Grade/bdde9d33956642129d82d219328ad5cc)](https://www.codacy.com/app/pltnk/selective_copy?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=pltnk/selective_copy&amp;utm_campaign=Badge_Grade)\n\nSimple command line application that copies all files with given extensions from a directory and its subfolders to another directory showing progress bar and remaining files counter.\\\nAllows to preserve a source folder structure, to process only files without given extensions, to move files instead of copying, to exclude certain files from processing and to create a log if necessary.\\\nOpens a filedialog if source and/or destination are not given in the command line.\\\nCreates folders in a destination path if they don't exist.\n\n## Installing\n\n<pre>\npip install slcp\n</pre>\n\nThis will install [version 0.1.0](https://github.com/pltnk/selective_copy/releases/tag/v0.1.0)\n\n## Usage\n\n<pre>\nslcp ext [ext ...] [-s SRC] [-d DST] [-sc | -dc] [-p] [-i] [-m] [-e FILE [FILE ...]] [-l] [-h]\n\nPositional arguments:\next                         One or more extensions of the files to copy. \n                            Enter extensions without a dot and separate by spaces.\n\nOptional arguments:\n-s SRC, --source SRC        Source folder path.\n-d DST, --dest DST          Destination folder path.\n-sc, --srccwd               Use current working directory as a source folder.\n-dc, --dstcwd               Use current working directory as a destination folder.\n-p, --preserve              Preserve source folder structure.\n-i, --invert                Process only files without given extensions.\n-m, --move                  Move files instead of copying, be careful with this option.\n-e FILE [FILE ...],         Exclude one or more files from processing.\n--exclude FILE [FILE ...]   Enter filenames with extensions and separate by spaces.\n-l, --log                   Create and save log to the destination folder.\n-h, --help                  Show this help message and exit.\n</pre>\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details\n\n## Acknowledgments\n\nInspired by the task from [Chapter 9 of Automate the Boring Stuff](https://automatetheboringstuff.com/chapter9/).\n",
    'author': 'Kirill Plotnikov',
    'author_email': 'kpltnk@gmail.com',
    'url': 'https://github.com/pltnk/selective_copy',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
