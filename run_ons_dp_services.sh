#!/bin/bash
SERVICES_CSV=${1-"ons-dp-web.csv"}
CURRENT_DIR=$(realpath $(dirname $0))
cd $CURRENT_DIR
source env/bin/activate
python -m run_ons_dp_services $SERVICES_CSV
