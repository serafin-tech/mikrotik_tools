#!/bin/bash

set -e

if [[ ! -d venv ]]
then
  python3 -m venv venv
fi

# shellcheck disable=SC1091
source venv/bin/activate

python3 -m pip install -U pip
python3 -m pip install -U -r requirements.txt

if [[ -f requirements-dev.txt ]]
then
  python3 -m pip install -U -r requirements-dev.txt
fi
