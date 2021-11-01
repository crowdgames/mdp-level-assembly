# gpcgrl

Graph Procedural Content Generation via Reinforcement Learning

* Setup: it is recommended to use [PyPy](https://www.pypy.org/) with pipenv for performance.
  * `pip3 install pipenv`
  * `pipenv --python pypy3 install`
  * `pipenv shell`

* First: create a graph file, either by n-grams or from a QD folder.
  * `python grams2graph.py ../TheVGLC/Super\ Mario\ Bros/Processed/mario-1-?.txt --gramsize 3 --out mario-grams.pkl`
  * `python qd2graph.py Mario --out mario-qd.pkl`
  * `python grams2graph.py ../TheVGLC/Kid\ Icarus/Processed/kidicarus_1.txt --gramsize 2 --transpose --out icarus-grams.pkl`

* Run comparisons of generation approaches.
  * `python graph_learn.py mario-grams.pkl --mario --blocksize 100 --comparetile "o"`
  * `python graph_learn.py mario-qd.pkl --mario --blocksize 100 --comparetile "["`
  * `python graph_learn.py icarus-grams.pkl --icarus --blocksize 50 --comparetile "T"`

* Run online learning and generation.
  * `python graph_learn.py mario-grams.pkl --blocksize 50 --mario --rungen`
  * `python graph_learn.py mario-qd.pkl --blocksize 50 --mario --rungen`
  * `python graph_learn.py icarus-grams.pkl --blocksize 20 --icarus --rungen`
  
* Generate random levels.
  * `python graph2level.py icarus-grams.pkl --size 50`

* Create a dot file of the graph.
  * `python graph2doy.py mario-grams.pkl`

* Get info about a graph.
  * `python graph2info.py mario-grams.pkl`
