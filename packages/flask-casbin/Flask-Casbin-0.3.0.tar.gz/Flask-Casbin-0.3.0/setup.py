# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_casbin']

package_data = \
{'': ['*']}

install_requires = \
['casbin>=1.1.2,<2.0.0', 'flask>=1.1,<2.0']

setup_kwargs = {
    'name': 'flask-casbin',
    'version': '0.3.0',
    'description': 'Flask Casbin Integration',
    'long_description': 'Flask-Casbin\n============\n\n[![Build Status](https://travis-ci.org/daymien/Flask-Casbin.png?branch=master)](https://travis-ci.org/daymien/Flask-Casbin)\n\n\nFlask-Casbin is an extension that provide Casbin ACL functionality to your Flask project\n\nInstallation\n------------\n\nInstall Flask-Casbin with `pip`:\n\n    pip install Flask-Casbin\n\nInstall Flask-Casbin with `poetry`:\n\n    poetry add Flask-Casbin\n\nExample\n-------\n\nThis is an example Flask application:\n\n```python\nfrom flask import Flask, abort\nfrom flask_casbin import CasbinManager, IOAdapter, current_enforcer\n\napp = Flask(__name__)\n\n# config\napp.config["CASBIN_MODEL_CONF"] = "./model.conf"\n\nacl = CasbinManager(app)\n\n@acl.policy_loader\ndef load_policy():\n    # some readable object for example based on current user\n    return IOAdapter(current_user.policy())\n\n@app.route(\'/data/<id_:int>\')\ndef get_data(id_):\n    # curent_user ist global authenticated user\n    current_enforcer.enforce(f"user:{current_user.name}", f"data:{id}", "read") or abort(401)\n    \n    # Get data\n    data = db.get_data(id_)\n    return { data_id: data.id, data: data.payload }\n\n```\n\nTodo\n----\n\n* Decorators for ACL check\n* ~Policy adapters~\n* ~Dynamic Policy Adapter (Flask-SQLAlchemy)~\n* More tests\n\nResources\n---------\n\n- [pypi](https://pypi.python.org/pypi/Flask-Casbin)\n- [casbin](https://casbin.org/)\n- [pycasbin](https://github.com/casbin/pycasbin)\n',
    'author': 'Reimund Klain',
    'author_email': 'reimund.klain@condevtec.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daymien/Flask-Casbin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
