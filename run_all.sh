#!/bin/bash

TYPE="--segment-graph"
RUNS="--runs 2"
TASK="--fit-persona"
GAME="--icarus"
SEGMENTS="--segments 3"
PLAYTHROUGHS="--playthroughs 20"
AGENT='--all'
# AGENT='--policy'

echo "pypy3 main.py --r-both ${GAME} ${TASK} ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"
screen -dm bash -c "pypy3 main.py --r-both ${GAME} ${TASK} ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"

echo "pypy3 main.py --r-player ${GAME} ${TASK}  ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"
screen -dm bash -c "pypy3 main.py --r-player ${GAME} ${TASK} ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"

echo "pypy3 main.py --r-designer ${GAME} ${TASK}  ${AGENT} ${RUNS} ${AGENT} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"
screen -dm bash -c "pypy3 main.py --r-designer ${GAME} ${TASK} ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"

TASK="--switch-persona"
echo "pypy3 main.py --r-both ${GAME} ${TASK} ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"  
screen -dm bash -c "pypy3 main.py --r-both ${GAME} ${TASK} ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}" 


# TYPE="--n-gram-graph"
# RUNS="--runs 5"
# TASK="--fit-persona"
# GAME="--mario"
# SEGMENTS="--segments 30"
# PLAYTHROUGHS="--playthroughs 50"
# AGENT='--all'

# echo "pypy3 main.py --r-both ${GAME} ${TASK}  ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"
# screen -dm bash -c "pypy3 main.py --r-both ${GAME} ${TASK}  ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"

# echo "pypy3 main.py --r-player ${GAME} ${TASK}  ${AGENT} ${RUNS}  ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"
# screen -dm bash -c "pypy3 main.py --r-player ${GAME} ${TASK}  ${AGENT} ${RUNS}  ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"

# echo "pypy3 main.py --r-designer ${GAME} ${TASK}  ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"
# screen -dm bash -c "pypy3 main.py --r-designer ${GAME} ${TASK}  ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"

# echo "all process started"
