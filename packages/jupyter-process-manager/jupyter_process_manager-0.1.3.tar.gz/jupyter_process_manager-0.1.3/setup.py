# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jupyter_process_manager']

package_data = \
{'': ['*']}

install_requires = \
['char>=0.1.2,<0.2.0',
 'ipywidgets>=7.6.3,<8.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'yaspin']

setup_kwargs = {
    'name': 'jupyter-process-manager',
    'version': '0.1.3',
    'description': 'python package with widget to simplify work with many processes in jupyter',
    'long_description': '=======================\njupyter_process_manager\n=======================\n\n.. image:: https://img.shields.io/github/last-commit/stas-prokopiev/jupyter_process_manager\n   :target: https://img.shields.io/github/last-commit/stas-prokopiev/jupyter_process_manager\n   :alt: GitHub last commit\n\n.. image:: https://img.shields.io/github/license/stas-prokopiev/jupyter_process_manager\n    :target: https://github.com/stas-prokopiev/jupyter_process_manager/blob/master/LICENSE.txt\n    :alt: GitHub license<space><space>\n\n.. image:: https://img.shields.io/pypi/v/jupyter_process_manager\n   :target: https://img.shields.io/pypi/v/jupyter_process_manager\n   :alt: PyPI\n\n.. image:: https://img.shields.io/pypi/pyversions/jupyter_process_manager\n   :target: https://img.shields.io/pypi/pyversions/jupyter_process_manager\n   :alt: PyPI - Python Version\n\n\n.. contents:: **Table of Contents**\n\nOverview.\n=========================\n\nThis is a library which helps working with many processes in a jupyter notebook in a very simple way.\n\nInstallation via pip:\n======================\n\n.. code-block:: bash\n\n    pip install jupyter_process_manager\n\n\nUsage examples\n===================================================================\n\nLets say that you want to run many processes with different arguments for the function below\n\n.. code-block:: python\n\n    def test_func(int_seconds):\n        for int_num in range(int_seconds):\n            print(int_num)\n            sleep(1)\n\nThen to run it you just need to do the following:\n\n.. code-block:: python\n\n    from jupyter_process_manager import JupyterProcessesManager\n    # Create an object which will be handling processes\n    process_manager = JupyterProcessesManager(".")\n\n    for wait_for_me in range(5, 50, 5):\n        process_manager.add_function_to_processing(test_func, wait_for_me)\n\n\nAll the processes were started and now you can check what is happening with them\n\nUsual print output\n--------------------------------------------------------------------------------------------------\n\n.. code-block:: python\n\n    process_manager.wait_till_all_processes_are_over(int_seconds_step=2)\n\n\n.. image:: images/1.PNG\n\n\nShow processes output as widget\n--------------------------------------------------------------------------------------------------\n\n.. code-block:: python\n\n    process_manager.show_jupyter_widget(\n        int_seconds_step=2,\n        int_max_processes_to_show=20\n    )\n\n.. image:: images/2.PNG\n\nJupyterProcessesManager arguments\n--------------------------------------------------------------------------------------------------\n\n#. **str_dir_for_output**: Directory where to store processes output\n#. **is_to_delete_previous_outputs=True**: Flag If you want to delete outputs for all previous processes in the directory\n\n\nLinks\n=====\n\n    * `PYPI <https://pypi.org/project/jupyter_process_manager/>`_\n    * `readthedocs <https://jupyter_process_manager.readthedocs.io/en/latest/>`_\n    * `GitHub <https://github.com/stas-prokopiev/jupyter_process_manager>`_\n\nProject local Links\n===================\n\n    * `CHANGELOG <https://github.com/stas-prokopiev/jupyter_process_manager/blob/master/CHANGELOG.rst>`_.\n\nContacts\n========\n\n    * Email: stas.prokopiev@gmail.com\n    * `vk.com <https://vk.com/stas.prokopyev>`_\n    * `Facebook <https://www.facebook.com/profile.php?id=100009380530321>`_\n\nLicense\n=======\n\nThis project is licensed under the MIT License.\n',
    'author': 'stanislav',
    'author_email': 'stas.prokopiev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
