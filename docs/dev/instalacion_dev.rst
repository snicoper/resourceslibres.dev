======================
Instalación Desarrollo
======================

Requerimientos sistema
======================

* PostgreSQL

Obtener repo de GitLab
======================

.. code-block:: bash

    cd ~/projects
    git clone git@gitlab.com:snicoper/resourceslibres.dev.git

Virtualenv
==========

.. code-block:: bash

    mkvirtualenv resourceslibres.dev

Editar arvhicos ``virtualenv``

.. code-block:: bash

    vim $VIRTUAL_ENV/bin/postactivate

    # Añadir
    source ~/projects/resourceslibres.dev/bin/postactivate.sh

.. code-block:: bash

    vim $VIRTUAL_ENV/bin/postdeactivate

    # Añadir
    source ~/projects/resourceslibres.dev/bin/postdeactivate.sh

Instalar paquetes **pip**

.. code-block:: bash

    pip install -r requirements/local.txt
    pip install -r requirements/prod.txt

Base de datos
=============

.. code-block:: bash

    psql -U postgres

    # Tener el usuario snicoper en ~/.pgpass
    CREATE USER snicoper WITH PASSWORD '123456';

reinstall_dev.sh
================

Ejecutando ``bin/reinstall_dev.sh`` ya se encarga de instalar ``npm`` y ``bower``, ademas de
crear la base de datos, etc.
