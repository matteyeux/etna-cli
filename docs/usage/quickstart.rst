..

quickstart
==========

Installation
------------


Make sure to have at least Python 3.7 and pip3 installed. Then run :
.. parsed-literal::

  pip3 install etna-cli


Also to use the task feature, you have to install taskwarror

.. content-tabs::

  .. tab-container:: tab1
    :title: Debian/Mint/Ubuntu

        .. code-block:: shell

            sudo apt install taskwarrior

  .. tab-container:: tab2
    :title: Fedora (Unix)

        .. code-block:: shell

            sudo dnf install task

  .. tab-container:: tab3
    :title: MacOS

        .. code-block:: shell

            brew install task





Configuration
-------------


To initialize configuration, you should first run:

.. code-block:: shell

    etna config init

It will ask for your etna ID and password. There is also an optional line where you can specify a Gitlab Token :

.. code-block:: shell

    λ ~ » etna config init    
    ETNA username : demo_a
    Password: 
    Add Gitlab API token ? [Y/n]: Y
    Gitlab API token :


.. note::
   The Python `keyrings` module is used to store passwords and tokens, which by default should use the keyring manager of your environment.
   Should you not like the default behavior, see https://pypi.org/project/keyring to get and configure alternative backends.


You can also edit some parts of the configuration using ``etna config edit``

.. code-block:: shell

    1 [credentials]
    2 username = hauteb_m
    3 
    4 [gitlab]
    5 url = https://rendu-git.etna-alternance.net
