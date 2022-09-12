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
PYTHON_ENV=$($PYTHON -c "import sys; sys.stdout.write('1') if hasattr(sys, 'real_prefix') else sys.stdout.write('0')")
[ $PYTHON_ENV = 1 ] && printGreen "Virtual environment activated" || ( printRed "Virtual environment activation failed"; exit 1 )

printWhite "Upgraging pip"
$PYTHON -m pip install --upgrade pip
[ $? = 0 ] && printGreen "Pip upgrated successfully" || ( printRed "Pip upgrade failed"; exit 1 )

printWhite "Installing packages"
pip install wheel auto-py-to-exe pyttsx3 aiorun colorama
[ $? = 0 ] && printGreen "Packages installed successfully" || ( printRed "Packages installation failed"; exit 1 )

printGreen "Environment is Ready"
deactivate