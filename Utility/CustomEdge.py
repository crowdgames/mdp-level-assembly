from dataclasses import dataclass
from GDM.Graph import Edge

@dataclass
class CustomEdge(Edge):
    sum_percent_complete: float = 0.0
    sum_visits: int = 0