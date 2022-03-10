#!/bin/bash

RUNS=10

echo "starting dungeongram processes"
screen -dm bash -c "pypy3 main.py --r-both --dungeongram --fit-persona --all --no-empty-link --runs ${RUNS}"
screen -dm bash -c "pypy3 main.py --r-player --dungeongram --fit-persona --all --no-empty-link --runs ${RUNS}"
screen -dm bash -c "pypy3 main.py --r-designer --dungeongram --fit-persona --all --no-empty-link --runs ${RUNS}"

echo "starting icarus processes"
screen -dm bash -c "pypy3 main.py --r-both --icarus --fit-persona --all --allow-empty-link --runs ${RUNS}"
screen -dm bash -c "pypy3 main.py --r-player --icarus --fit-persona --all --allow-empty-link --runs ${RUNS}"
screen -dm bash -c "pypy3 main.py --r-designer --icarus --fit-persona --all --allow-empty-link --runs ${RUNS}"

echo "starting mario processes"
screen -dm bash -c "pypy3 main.py --r-both --mario --fit-persona --all --allow-empty-link --runs ${RUNS}"
screen -dm bash -c "pypy3 main.py --r-player --mario --fit-persona --all --allow-empty-link --runs ${RUNS}"
screen -dm bash -c "pypy3 main.py --r-designer --mario --fit-persona --all --allow-empty-link --runs ${RUNS}"

echo "all process started"
