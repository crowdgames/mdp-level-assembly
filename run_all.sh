#!/bin/bash

RUNS=10
TASK="--fit-persona"
# TASK="--fit-agent"

echo "starting dungeongram processes"
screen -dm bash -c "pypy3 main.py --r-both --dungeongram ${TASK} --all --no-empty-link --runs ${RUNS}"
screen -dm bash -c "pypy3 main.py --r-player --dungeongram ${TASK} --all --no-empty-link --runs ${RUNS}"
screen -dm bash -c "pypy3 main.py --r-designer --dungeongram ${TASK} --all --no-empty-link --runs ${RUNS}"

echo "starting icarus processes"
screen -dm bash -c "pypy3 main.py --r-both --icarus ${TASK} --all --allow-empty-link --runs ${RUNS}"
screen -dm bash -c "pypy3 main.py --r-player --icarus ${TASK} --all --allow-empty-link --runs ${RUNS}"
screen -dm bash -c "pypy3 main.py --r-designer --icarus ${TASK} --all --allow-empty-link --runs ${RUNS}"

echo "starting mario processes"
screen -dm bash -c "pypy3 main.py --r-both --mario ${TASK} --all --allow-empty-link --runs ${RUNS}"
screen -dm bash -c "pypy3 main.py --r-player --mario ${TASK} --all --allow-empty-link --runs ${RUNS}"
screen -dm bash -c "pypy3 main.py --r-designer --mario ${TASK} --all --allow-empty-link --runs ${RUNS}"

echo "all process started"
