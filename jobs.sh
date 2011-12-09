#!/usr/bin/env bash

set -e
PROJDIR=/mnt/projects/eyerisserver
. ${PROJDIR}/env/bin/activate
cd /mnt/projects/eyerisserver/releases/current/eyerisserver
export DJANGO_SETTINGS_MODULE=settings
export PYTHONPATH=${PYTHONPATH}:`pwd`:`pwd`/..
export PRODUCTION=TRUE

rm -rf data
mkdir -p data
well_shapefile_url=http://cogcc.state.co.us/Downloads/WELL_SHP.ZIP
apermit_shapefile_url=http://cogcc.state.co.us/Downloads/PERMIT_S.ZIP
well_shapefile=$(basename $well_shapefile_url)
apermit_shapefile=$(basename $apermit_shapefile_url)

wget $well_shapefile_url -O data/$well_shapefile
wget $apermit_shapefile_url -O data/$apermit_shapefile

unzip data/$well_shapefile -d data
unzip data/$apermit_shapefile -d data

python -c "import app.imports"