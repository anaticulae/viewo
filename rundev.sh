#! /usr/bin/bash

export FLASK_APP=viewo.app:create_app
export FLASK_ENV=development

python -m flask run &
