# gpcgrl

Graph Procedural Content Generation via Reinforcement Learning


`

## Use

We recommended to using [PyPy](https://www.pypy.org/) with pipenv for performance.

```bash
pip3 install pipenv
pipenv --python pypy3 install
pipenv shell
```

To re-run all experiments, run `./run_all.sh`. To run, use the following command and fill in however you please. Use `pypy3 main.ph --help` for instructions on possible discrete values. Most values also have default values.

```
pypy3 main.py ${REWARD} ${GAME} ${TASK} ${AGENT} --runs ${RUNS} --segments ${SEGMENTS} ${TYPE} --playthroughs ${PLAYTHROUGHS}
```

## Unit Test

```
pypy3 -m unittest
```

## Future Work

Binary search like approach to selecting the next level. If the user lost, select the visited node between the easiest difficulty possible and the hardest level from the level selection they just played.


Visited nodes should be nodes that the player fails to beat