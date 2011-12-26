#!/bin/sh

export PRODUCTION=TRUE
. /mnt/projects/eyerisserver/env/bin/activate
cd /mnt/projects/eyerisserver/releases/current/eyerisserver
# The --noinput versin of this still requires a eventual password prompt 
# with a later call to createsuperuser
./manage.py syncdb
./manage.py collectstatic --noinput


