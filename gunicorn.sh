#!/bin/bash
set -e
PROJDIR=/mnt/projects/eyerisserver
LOGFILE=/mnt/projects/eyerisserver_gunicorn.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
# user/group to run as
USER=www-data
GROUP=www-data

source ${PROJDIR}/env/bin/activate
export PRODUCTION=TRUE

cd /mnt/projects/eyerisserver/releases/current/eyerisserver
exec gunicorn_django -w $NUM_WORKERS \
    --user=$USER --group=$GROUP --log-level=debug \
    --log-file=$LOGFILE --bind 127.0.0.1:8001 2>>$LOGFILE
