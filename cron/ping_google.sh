#!/bin/bash

source $HOME/.bashrc

workon "resourceslibres.com"

source _variables.sh

python $PROJECT_ROOT/ping_google.py
