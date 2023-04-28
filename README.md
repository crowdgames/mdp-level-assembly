# Level Assembly as a Markov Decision Process

## Abstract

Many games feature a progression of levels that does not change or adapt to the player. This can be problematic because some players may get stuck if the progression is too difficult and others may find it boring if it is too slow to get to more challenging levels. One way to address this is to build levels based on the player's performance and preferences. In this work, we formulate the problem of generating levels for a player as a Markov Decision Process (MDP) and use adaptive dynamic programming (ADP) to solve the MDP before assembling a level. We tested with two case studies and find that using an ADP outperforms two baselines. Furthermore, we tested with player proxies and switched them in the middle of play, and we show that a simple modification prior to running an ADP results in quick adaptation. By using an ADP, which searches the entire MDP, we produce a dynamic progression of levels that adapts to the player.

## Paper

A free to read version of the paper can be found on [arxiv](https://arxiv.org/pdf/2304.13922v1.pdf).

## Use

We recommended to using [PyPy](https://www.pypy.org/) with pipenv for performance.

```bash
pip3 install pipenv
pipenv --python pypy3 install
pipenv shell
```

One dependency is [GDM](https://github.com/bi3mer/GDM), which is a small library I wrote for defining and running an MDP. To re-run all experiments, run `./run_all.sh`. To run, use the following command and fill in however you please. Use `pypy3 main.ph --help` for instructions on possible discrete values. Most values have default values.

```
pypy3 main.py ${REWARD} ${GAME} ${TASK} ${AGENT} --runs ${RUNS} --segments ${SEGMENTS} ${TYPE} --playthroughs ${PLAYTHROUGHS}
```
