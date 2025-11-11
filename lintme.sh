#!/bin/bash

if [ ! -d venv ]
then
    echo "MIssing venv directory, run venv_setup.sh"
    exit 1
fi

. venv/bin/activate

pylint $(git ls-files '*.py')
