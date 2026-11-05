#! /usr/bin/bash

export VIEWO_TMP="${SHARED_SPACE:-$HOME/.tmp/viewo}"

export SHARED_SPACE="${SHARED_SPACE:-$VIEWO_TMP/shared}"
export SHARED_TMP="${SHARED_TMP:-$SHARED_SPACE/tmp}"
export SHARED_TODO="${SHARED_TODO:-$SHARED_SPACE/todo}"
export SHARED_READY="${SHARED_READY:-$SHARED_SPACE/ready}"

export VIEWO_HELPDESK="${VIEWO_HELPDESK:-$VIEWO_TMP/helpdesk}"

mkdir -p $SHARED_READY $SHARED_TMP $SHARED_TODO $VIEWO_HELPDESK

export FLASK_APP=viewo.app:create_app
export FLASK_ENV=development

python -m flask run &
