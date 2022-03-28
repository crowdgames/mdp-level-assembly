#!/bin/bash

# TYPE="--segment-graph"
# RUNS=20
# TASK="--fit-persona"
# GAME="--mario"
# SEGMENTS=5

TYPE="--n-gram-graph"
RUNS=100
TASK="--fit-persona"
GAME="--icarus"
SEGMENTS=40
PLAYTHROUGHS="--playthroughs 100"


screen -dm bash -c "pypy3 main.py --r-both ${GAME} ${TASK} --all --runs ${RUNS} --segments ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"
screen -dm bash -c "pypy3 main.py --r-player ${GAME} ${TASK} --all --runs ${RUNS} --segments ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"
screen -dm bash -c "pypy3 main.py --r-designer ${GAME} ${TASK} --all  --runs ${RUNS} --segments ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"

echo "all process started"
