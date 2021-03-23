#!/bin/bash

N_WORKERS=$1
PY_SCRIPT=$2

for i in $(seq 1 $N_WORKERS)
do
	locust -f $PY_SCRIPT --worker --master-host=127.0.0.1 &
done
