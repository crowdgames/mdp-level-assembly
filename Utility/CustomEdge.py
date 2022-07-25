from dataclasses import dataclass
from GDM.Graph import Edge

@dataclass
class CustomEdge(Edge):
    sum_percent_complete: float = 0.8
    sum_visits: int = 1