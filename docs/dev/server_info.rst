==========================
Configuraciones del Server
==========================

**ip:** 94.177.235.146

============
Requirements
============

* Post instalacion Centos 7.
* Configurar SSH.
* PostgreSQL 9.6.
* Python34 de epel.
* Nginx.
* Certificado SSL certbot.
* Postfix.
* Nodejs, los repos de nodejs.
* bower, gulp, node-sass global.

hostname
========

.. code-block:: bash

    hostnamectl --static set-hostname ns1.resourceslibres.com

firewalld
=========

Por defecto no viene instalado (en aruba)

.. code-block:: bash

    yum install firewalld

Importante abrir el puerto antes de cambiar la configuración de ``ssh``.

.. code-block:: bash

    # IMPORTANTE
    firewall-cmd --permanent --zone=public --add-port=6543/tcp

SELinux
=======

Por defecto en Aruba viene desactivado, no activar y omitir este paso.

En caso de configurarlo.

.. code-block:: bash

    vim /etc/sysconfig/selinux

    # Editar
    SELINUX=enforcing

    # IMPORTANTE
    semanage port -a -t ssh_port_t -p tcp 6543

    reboot

Usuarios y grupos
=================

Tener creados usuarios ``snicoper`` y ``weberrors``, ver ``secrets`` para los passwords.

Añadir ``snicoper`` al grupo ``webapps``

.. code-block:: bash

    groupadd webapps
    usermod -a -G webapps snicoper

Notas de Firewalld
==================

IMPORTANTE: Tener ya configurado ``ssh``

.. code-block:: bash

    # ssh
    firewall-cmd --permanent --zone=public --add-port=6543/tcp
    firewall-cmd --permanent --zone=public --remove-service=ssh
    firewall-cmd --permanent --zone=public --add-service=http
    firewall-cmd --permanent --zone=public --add-service=https
    firewall-cmd --permanent --zone=public --add-service=smtp
    firewall-cmd --permanent --zone=public --add-service=imaps

    firewall-cmd --reload

    firewall-cmd --zone=public --list-all

Notas para PostgreSQL 9.6
=========================

* http://www.postgresonline.com/journal/archives/362-An-almost-idiots-guide-to-install-PostgreSQL-9.5,-PostGIS-2.2-and-pgRouting-2.1.0-with-Yum.html

.. code-block:: bash

    yum install https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-7-x86_64/pgdg-centos96-9.6-3.noarch.rpm

    yum install postgresql96 postgresql96-server postgresql96-devel postgresql96-contrib

Como es la unica version de PostgreSQL, añadir al **PATH**.

.. code-block:: bash

    vim /etc/profile

    export PATH="$PATH:/usr/pgsql-9.6/bin/"

    # Reinicar

    postgresql96-setup initdb
    systemctl start postgresql-9.6
    systemctl enable postgresql-9.6

    # Añadir contraseña a postgres.
    su - postgres
    psql
    \password postgres
    \q
    exit

Archivos de configuración

.. code-block:: bash

    vim /var/lib/pgsql/9.6/data/postgresql.conf
    vim /var/lib/pgsql/9.6/data/pg_hba.conf

Notas Python34
==============

.. code-block:: bash

    yum install python34 python34-setuptools python34-devel redhat-rpm-config

    curl https://bootstrap.pypa.io/get-pip.py | python3.4

Notas postfix
=============

Sobre escribir la configuración que tengo de instalación postfix

En ``vim /etc/postfix/main.cf``

.. code-block:: bash

    smtpd_tls_cert_file = /etc/letsencrypt/live/resourceslibres.com/fullchain.pem
    smtpd_tls_key_file = /etc/letsencrypt/live/resourceslibres.com/privkey.pem

Y en ``/etc/dovecot/conf.d/10-ssl.conf``

.. code-block:: bash

    ssl_cert = </etc/letsencrypt/live/resourceslibres.com/fullchain.pem
    ssl_key = </etc/letsencrypt/live/resourceslibres.com/privkey.pem

.bashrc
=======

Usuario **snicoper**

.. code-block:: bash

    parse_git_branch() {
         git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
    }

    export PS1="\e[32m\u at \e[34m$(hostname -f) \e[32m\w\[\033[33m\]\$(parse_git_branch)\[\033[00m\] \n$ "

    # Virtualenvwrapper
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
    export WORKON_HOME=$HOME/.virtualenvs
    source /usr/bin/virtualenvwrapper.sh

Usuario **root**

.. code-block:: bash

    parse_git_branch() {
         git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
    }

    # Para root
    export PS1="\e[31m\u at \e[34m$(hostname -f) \e[31m\w\\e[31m\$(parse_git_branch)\[\033[00m\] \n$ "

.gitconfig
==========

.. code-block:: bash

    [user]
      name = Salvador Nicolas
      email = snicoper@gmail.com
    [color]
      ui = true
    [core]
      editor = vim
    [alias]
      lg = log --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr %an)%Creset' --abbrev-commit --date=relative
      co = checkout
      cm = commit
      st = status
      br = branch

vimrc
=====

.. code-block:: bash

    vim ~/.vimrc

.. code-block:: viml

    set pastetoggle=<F2>
    set clipboard=unnamed
    set encoding=utf8

    " Rebind <Leader> key
    let mapleader = ","

    " Enable syntax highlighting
    " You need to reload this file for the change to apply
    filetype off
    filetype plugin indent on
    syntax on
    set scrolloff=8

    " Showing line length
    set nonu
    set tw=79   " width of document (used by gd)
    set nowrap  " don't automatically wrap on load
    set fo-=t   " don't automatically wrap text when typing
    set colorcolumn=100
    highlight ColorColumn ctermbg=233

    " Useful settings
    set history=700
    set undolevels=700

    " Real programmers don't use TABs but spaces
    autocmd Filetype python setlocal expandtab tabstop=4 shiftwidth=4
    autocmd Filetype md setlocal expandtab tabstop=4 shiftwidth=4
    autocmd Filetype rst setlocal expandtab tabstop=4 shiftwidth=4
    set tabstop=2
    set softtabstop=2
    set shiftwidth=2
    set shiftround
    set expandtab

    " Make search case insensitive
    set hlsearch
    set incsearch
    set ignorecase
    set smartcase

    " Disable stupid backup and swap files - they trigger too many events
    " for file system watchers
    set nobackup
    set nowritebackup
    set noswapfile

    " Split navigations
    nnoremap <C-J> <C-W><C-J>
    nnoremap <C-K> <C-W><C-K>
    nnoremap <C-L> <C-W><C-L>
    nnoremap <C-H> <C-W><C-H>

    " Stupid shift key fixes
    command! -bang -nargs=* -complete=file E e<bang> <args>
    command! -bang -nargs=* -complete=file W w<bang> <args>
    command! -bang -nargs=* -complete=file Wq wq<bang> <args>
    command! -bang -nargs=* -complete=file WQ wq<bang> <args>
    command! -bang Wa wa<bang>
    command! -bang WA wa<bang>
    command! -bang Q q<bang>
    command! -bang QA qa<bang>
    command! -bang Qa qa<bang>

Copiar ``.vimrc`` a **root**

.. code-block:: bash

    sudo cp /home/snicoper/.vimrc /root/.vimrc

