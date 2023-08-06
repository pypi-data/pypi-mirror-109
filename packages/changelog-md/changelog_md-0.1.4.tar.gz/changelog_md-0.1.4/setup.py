# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['changelog_md']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'changelog-md',
    'version': '0.1.4',
    'description': 'A package to create changelogs for your git tracked projects.',
    'long_description': '# install with pip\n```bash\npython3 -m pip install changelog-md\n``` \n\n# install with Poetry\n```\npoetry add changelog-md\n```\n\n# execution information:\n\nThis script aim to provide changelogs on git-tracked projects.\nRun `changelog.py` script in your directory \nand it\'ll generate the changelog file.\nIn order to obtain actual changelog, run:\n\n\nYou can use git changelog from command line directly:\n```bash\n# ... code on project\ngit commit                                                    #add your commit message on work you\'ve done\npython3 -m changelog_md vX.Y.Z "Annotation for this version" #generate changelog\ngit add changelog.md                                          #stage the changelog to current commit\ngit commit --amend                                            #add the changelog to current commit, leave commit message as is.\ngit tag -a vX.Y.Z -m "Annotation for this version"            #add the tag you\'ve set earlier in changelog.\ngit push --follow-tags                                        #publish your changes and the new tag.\n```\n\nOr you can elaborate your workflow python scripts \nto use changelog_md as a python module:\n```python\n# CICD_script.py\n# ... do some CICD work\n\nfrom changelog_md import logger\nl = logger(\'vX.Y.Z\', \'Annotation for this version\')           #create logger instance\nl.make()                                                      #print the log\n\n# ... do other CICD work\n```\n\n\nMore actual information on colophon of scripts:\n```shell\n#actual information on colophon:\npython3 -m changelog_md --help\n```\n\n# correct commit messages:\n\nTo make this scripts work properly, your commit messages\nshould look like any of this:\n```\n[feature] feature description here\n[fix] fix description\n[changelog] minor changes description\n[internal] this section will be generated only if --internal argument is given.\nThis commit message string will be ommited from changelog.\n```\n\n#  Releases:\n\nAny tagged commit will be interpreted as release.\nTo create tag, write:\n```\ngit tag -a v<version>\n... tag anotation ...\ngit push --follow-tags\n```\nAny commit above the last tag will be marked as tag provided \nin command line arguments and annotated accordingly.\n',
    'author': 'Ruslan Sergeev',
    'author_email': 'mybox.sergeev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RuslanSergeev/git_changelog',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
