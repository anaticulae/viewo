#! /usr/bin/bash

export FLASK_APP=viewo/app.py
export FLASK_ENV=development

python -m flask run &
