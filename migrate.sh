#!/bin/sh

export PRODUCTION=TRUE
. /mnt/projects/eyerisserver/env/bin/activate
cd /mnt/projects/eyerisserver/releases/current/eyerisserver
./manage.py migrate app


