# gpcgrl

Graph Procedural Content Generation via Reinforcement Learning

* First: create a graph file, either by n-grams or from a QD folder.
  * `pypy3 grams2graph.py ../TheVGLC/Super\ Mario\ Bros/Processed/mario-1-?.txt --gramsize 3 --out mario-grams.pkl`
  * `pypy3 qd2graph.py Mario --out mario-qd.pkl`
  * `pypy3 grams2graph.py ../TheVGLC/Kid\ Icarus/Processed/kidicarus_1.txt --gramsize 2 --transpose --out icarus-grams.pkl`

* Run comparisons of generation approaches.
  * `pypy3 graph_learn.py mario-grams.pkl --mario --blocksize 100 --comparetile "o"`
  * `pypy3 graph_learn.py mario-qd.pkl --mario --blocksize 100 --comparetile "["`
  * `pypy3 graph_learn.py icarus-grams.pkl --icarus --blocksize 50 --comparetile "T"`

* Run online learning and generation.
  * `pypy3 graph_learn.py mario-grams.pkl --blocksize 50 --mario --rungen`
  * `pypy3 graph_learn.py mario-qd.pkl --blocksize 50 --mario --rungen`
  * `pypy3 graph_learn.py icarus-grams.pkl --blocksize 20 --icarus --rungen`
  
* Generate random levels.
  * `pypy3 graph2level.py icarus-grams.pkl --size 50`

* Create a dot file of the graph.
  * `pypy3 graph2doy.py mario-grams.pkl`
