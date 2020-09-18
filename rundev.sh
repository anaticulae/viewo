#! /usr/bin/bash

export FLASK_APP=viewo/__main__.py
export FLASK_ENV=development

python -m flask run &
