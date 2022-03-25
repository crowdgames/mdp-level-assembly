#!/bin/bash

RUNS=20
TASK="--fit-persona"
GAME="--mario"
SEGMENTS=5
# TASK="--fit-agent"

screen -dm bash -c "pypy3 main.py --r-both ${GAME} ${TASK} --all --runs ${RUNS} --segments ${SEGMENTS}"
screen -dm bash -c "pypy3 main.py --r-player ${GAME} ${TASK} --all --runs ${RUNS} --segments ${SEGMENTS}"
screen -dm bash -c "pypy3 main.py --r-designer ${GAME} ${TASK} --all  --runs ${RUNS} --segments ${SEGMENTS}"

echo "all process started"
