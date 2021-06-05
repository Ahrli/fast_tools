#!/bin/sh

# install python lib
if [ -e "/requirements.txt" ]; then
    $(which pip) install --user -r /requirements.txt
fi

python3 /ENIAC/app.py