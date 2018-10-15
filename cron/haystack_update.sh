#!/bin/bash

source $HOME/.bashrc

workon "resourceslibres.com"

source _variables.sh

$PROJECT_ROOT/prod_manage.py update_index
