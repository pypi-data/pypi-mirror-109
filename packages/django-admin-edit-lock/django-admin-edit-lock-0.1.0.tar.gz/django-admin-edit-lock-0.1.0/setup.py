# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['admin_edit_lock']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2']

setup_kwargs = {
    'name': 'django-admin-edit-lock',
    'version': '0.1.0',
    'description': 'django-admin-edit-lock is a Django application used in admin to prevent simultaneous edit by more than one users.',
    'long_description': '# django-admin-edit-lock\n\n## Setup\nInstall package using `pip`:\n\n```shell\npython -m pip install django-admin-edit-lock\n```\n\nAdd it to the installed apps:\n```python\nINSTALLED_APPS = [\n    ...\n    "admin_edit_lock",\n    ...\n]\n```\n\n## Configuration\nThe is one mandatory setting `ADMIN_EDIT_LOCK_DURATION` which defines how long the edit lock should last. The value is in seconds. For example:\n\n```python\nADMIN_EDIT_LOCK_DURATION = 10 * 60\n```\n\nwill keep the lock for ten minutes.\n\n## Roadmap\n- Customize messages\n- Extending the lock expiry time through AJAX call\n- Optionally set a limit to how much the lock can be extended\n\n## Credits\nThis project is inspired by https://github.com/jonasundderwolf/django-admin-locking . This project differentiates by utilizing the Django permissions to decide whether a user can edit or not. Further, this project uses the messages middleware is used to notify the users of the lock status.',
    'author': 'Demetris Stavrou',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/demestav/django-admin-edit-lock',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
