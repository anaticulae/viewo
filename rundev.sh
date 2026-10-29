#! /usr/bin/bash

export SHARED_SPACE="${SHARED_SPACE:-$HOME/.tmp/viewo/shared}"
export SHARED_TMP="${SHARED_TMP:-$SHARED_SPACE/tmp}"
export SHARED_TODO="${SHARED_TODO:-$SHARED_SPACE/todo}"
export SHARED_READY="${SHARED_READY:-$SHARED_SPACE/ready}"

mkdir -p $SHARED_READY $SHARED_TMP $SHARED_TODO

export FLASK_APP=viewo.app:create_app
export FLASK_ENV=development

python -m flask run &
