=========================
Instalación en Producción
=========================

Certificado SSL
===============

Para crear el certificado, hacerlo sin configuración del server. Con Nginx recién instalado
o renombrar ``/etc/nginx/conf.d/resourceslibres.com.conf`` a ``/etc/nginx/conf.d/resourceslibres.com``

El email **snicoper@gmail.com**

**Fuentes:**

https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-centos-7

.. code-block:: bash

    yum install certbot

.. code-block:: conf

    vim /etc/nginx/default.d/le-well-known.conf

.. code-block:: conf

    location ~ /.well-known {
      allow all;
    }

    systemctl restart nginx

.. code-block:: bash

    certbot certonly -a webroot --webroot-path=/usr/share/nginx/html -d resourceslibres.com -d www.resourceslibres.com -d mail.resourceslibres.com

Cuando todo haya salido bien

.. code-block:: bash

    openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048

Actualizar el certificado, dura 3 meses.

.. code-block:: bash

    certbot renew

Ver al final ``cron`` para actualizar.

Database
========

Añadir a ``.pgpass``

.. code-block:: console

    vim ~/.pgpass

    # Añadir
    localhost:5432:*:postgres:123456!
    localhost:5432:resourceslibrescom:resourceslibrescom:123456

    # Permisos
    chmod 600 ~/.pgpass

Crear el usuario en la db.

.. code-block:: psql

    psql -U postgres -c "CREATE USER resourceslibrescom WITH PASSWORD '123456';"
    psql -U postgres -c "CREATE DATABASE resourceslibrescom WITH OWNER resourceslibrescom;"

Restaurar **backup** de la db.

.. code-block:: psql

    # Producción
    psql -U postgres resourceslibrescom < backups/postgresql/archivo_restauracion.sql
    \q

Sources y Virtualenv
====================

.. code-block:: bash

    mkdir /var/webapps
    cd /var
    chown -R snicoper:webapps webapps
    cd webapps

    git clone git@gitlab.com:snicoper/resourceslibres.dev.git resourceslibres.com

    cd resourceslibres.com/

    git pull origin prod
    git checkout prod

    mkvirtualenv resourceslibres.com

    vim $VIRTUAL_ENV/bin/postactivate

    source /var/webapps/resourceslibres.com/bin/postactivate.sh

    deactivate
    workon resourceslibres.com

    vim $VIRTUAL_ENV/bin/postdeactivate

    source /var/webapps/resourceslibres.com/bin/postdeactivate.sh

Install requirements pip

.. code-block:: bash

    pip install -r requirements/prod.txt

Nginx host virtual
==================

Editar ``compose/configs/nginx.conf`` 178 aprox poner ip publica del servidor.

.. code-block:: bash

    sudo cp compose/configs/nginx.conf /etc/nginx/conf.d/resourceslibres.com.conf

    sudo vim /etc/nginx/nginx.conf

    # Aliminar linea 39 y 40
    default_server

    sudo systemctl restart nginx.service

Gunicorn
========

Crear un servicio systemd para Gunicorn

.. code-block:: bash

    sudo cp compose/configs/gunicorn.service /etc/systemd/system/gunicorn.service
    sudo cp compose/configs/logrotate /etc/logrotate.d/gunicorn
    sudo mkdir /var/log/gunicorn/
    sudo chown snicoper:webapps /var/log/gunicorn/
    sudo systemctl start gunicorn.service
    sudo systemctl enable gunicorn.service

NPM y bower
===========

.. code-block:: bash

    cd_project

    npm install
    bower install

staticfiles
===========

.. code-block:: bash

    workon resourceslibres.com
    cd_project

    ./prod_manage.py collectstatic

Cron
====

Requiere ``ssh-copy-id`` para ``rsync`` y tener ``sshd`` ``enable`` y ``start``

.. code-block:: bash

    sudo cp compose/configs/cron_root /var/spool/cron/root
    sudo cp compose/configs/cron_snicoper /var/spool/cron/snicoper

Haystack
========

Generar archivo.

.. code-block:: bash

    ./prod_manage.py rebuild_index

Después ya con cron se encarga de ir actualizándolos.
