#!/bin/bash

if [[ ! -d venv ]]
then
    echo "MIssing venv directory, run venv_setup.sh"
    exit 1
fi

. venv/bin/activate

pip3 install -U pylint

pylint $(git ls-files '*.py')
