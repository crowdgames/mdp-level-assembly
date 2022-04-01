# #!/bin/bash

TYPE="--segment-graph"
RUNS="--runs 100"
TASK="--fit-persona"
GAME="--icarus"
SEGMENTS="--segments 5"
PLAYTHROUGHS="--playthroughs 50"
AGENT='--all'

echo "pypy3 main.py --r-both ${GAME} ${TASK} ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"
screen -dm bash -c "pypy3 main.py --r-both ${GAME} ${TASK} ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"

echo "pypy3 main.py --r-player ${GAME} ${TASK}  ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"
screen -dm bash -c "pypy3 main.py --r-player ${GAME} ${TASK} ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"

echo "pypy3 main.py --r-designer ${GAME} ${TASK}  ${AGENT} ${RUNS} ${AGENT} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"
screen -dm bash -c "pypy3 main.py --r-designer ${GAME} ${TASK} ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"

TASK="--switch-persona"
echo "pypy3 main.py --r-both ${GAME} ${TASK} ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"  
screen -dm bash -c "pypy3 main.py --r-both ${GAME} ${TASK} ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}" 


TYPE="--n-gram-graph"
RUNS="--runs 100"
TASK="--fit-persona"
GAME="--mario"
SEGMENTS="--segments 40"
PLAYTHROUGHS="--playthroughs 100"
AGENT='--all'

echo "pypy3 main.py --r-both ${GAME} ${TASK}  ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"
screen -dm bash -c "pypy3 main.py --r-both ${GAME} ${TASK}  ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"

echo "pypy3 main.py --r-player ${GAME} ${TASK}  ${AGENT} ${RUNS}  ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"
screen -dm bash -c "pypy3 main.py --r-player ${GAME} ${TASK}  ${AGENT} ${RUNS}  ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"

echo "pypy3 main.py --r-designer ${GAME} ${TASK}  ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"
screen -dm bash -c "pypy3 main.py --r-designer ${GAME} ${TASK}  ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"

echo "all process started"
