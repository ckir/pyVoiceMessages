#!/bin/bash
set -e
me="$(basename "$(test -L "$0" && readlink "$0" || echo "$0")")"
source color_print.sh

if [ $# -eq 0 ]
  then
    printRed "Usage: $0 <full path to python executable>"
    exit 1
fi

PYTHON=$1
if ! command -v $PYTHON &> /dev/null
then
    printRed "$PYTHON could not be found"
    exit 1
fi

version=`$PYTHON --version`
if ! [[ $version == Python* ]]
then
    printRed "Cannot determine Python's version"
    exit 1
fi
printWhite "You are using $version"

printWhite "Cleaning old virtual environment"
if [ -d "venv" ]; then rm -Rf "venv"; fi

printWhite "Creating virtual environment"
$PYTHON -m venv venv
[ $? = 0 ] && printGreen "Virtual environment created successfully" || ( printRed "Virtual environment build failed"; exit 1 )

source venv/bin/activate
PYTHON_ENV=$(python3 -c "import sys; print(hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))")
[ $PYTHON_ENV != "False" ] && printGreen "Virtual environment activated" || ( printRed "Virtual environment activation failed"; exit 1 )

printWhite "Upgraging pip"
pip install --upgrade pip
[ $? = 0 ] && printGreen "Pip upgrated successfully" || ( printRed "Pip upgrade failed"; exit 1 )

printWhite "Installing packages"
pip install wheel auto-py-to-exe pyttsx3 aiorun colorama
[ $? = 0 ] && printGreen "Packages installed successfully" || ( printRed "Packages installation failed"; exit 1 )

printGreen "Environment is Ready"
deactivate
