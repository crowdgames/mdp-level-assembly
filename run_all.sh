#!/bin/bash

TYPE="--segment-graph"
TASK="--fit-persona"
GAME="--icarus"
RUNS="--runs 20"
PLAYTHROUGHS="--playthroughs 50"
SEGMENTS="--segments 5"

# echo "pypy3 main.py --r-both ${GAME} ${TASK} --policy ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"
# screen -dm bash -c "pypy3 main.py --r-both ${GAME} ${TASK} --policy ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"

# echo "pypy3 main.py --r-both ${GAME} ${TASK} --adaptive-policy ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"
# screen -dm bash -c "pypy3 main.py --r-both ${GAME} ${TASK} --adaptive-policy ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"

# echo "pypy3 main.py --r-both ${GAME} ${TASK} --greedy ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"
# screen -dm bash -c "pypy3 main.py --r-both ${GAME} ${TASK} --greedy ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"

# echo "pypy3 main.py --r-both ${GAME} ${TASK} --random ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"
# screen -dm bash -c "pypy3 main.py --r-both ${GAME} ${TASK} --random ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"

# TASK="--switch-persona"
# echo "pypy3 main.py --r-both ${GAME} ${TASK} --policy ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"  
# screen -dm bash -c "pypy3 main.py --r-both ${GAME} ${TASK} --policy ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}" 

# echo "pypy3 main.py --r-both ${GAME} ${TASK} --adaptive-policy ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"  
# screen -dm bash -c "pypy3 main.py --r-both ${GAME} ${TASK} --adaptive-policy ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}" 

# echo "pypy3 main.py --r-both ${GAME} ${TASK} --random ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"  
# screen -dm bash -c "pypy3 main.py --r-both ${GAME} ${TASK} --random ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}" 

# echo "pypy3 main.py --r-both ${GAME} ${TASK} --greedy ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"  
# screen -dm bash -c "pypy3 main.py --r-both ${GAME} ${TASK} --greedy ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}" 


# n-gram is much faster overall
TYPE="--n-gram-graph"
RUNS="--runs 20"
TASK="--fit-persona"
GAME="--mario"
SEGMENTS="--segments 30"
PLAYTHROUGHS="--playthroughs 20"
AGENT='--all'

echo "pypy3 main.py --r-both ${GAME} ${TASK}  ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"
screen -dm bash -c "pypy3 main.py --r-both ${GAME} ${TASK}  ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"

echo "pypy3 main.py --r-player ${GAME} ${TASK}  ${AGENT} ${RUNS}  ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"
screen -dm bash -c "pypy3 main.py --r-player ${GAME} ${TASK}  ${AGENT} ${RUNS}  ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"

echo "pypy3 main.py --r-designer ${GAME} ${TASK}  ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"
screen -dm bash -c "pypy3 main.py --r-designer ${GAME} ${TASK}  ${AGENT} ${RUNS} ${SEGMENTS} ${TYPE} ${PLAYTHROUGHS}"

echo "all process started"
