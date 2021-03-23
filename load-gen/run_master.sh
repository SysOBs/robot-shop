#!/bin/bash

PY_SCRIPT=$1
HOST=$2
N_CLIENTS=$3
SPAWN_RATE=$4

locust -f $PY_SCRIPT --master --host $HOST -u $N_CLIENTS -r $SPAWN_RATE
