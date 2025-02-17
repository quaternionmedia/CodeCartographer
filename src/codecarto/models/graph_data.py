from networkx import DiGraph
from pydantic import BaseModel

from models.source_data import File, Folder


class Edge(BaseModel):
    id: int
    type: str = ""
    source: int
    target: int


class Node(BaseModel):
    id: int
    type: str
    filename: str = ""
    label: str = ""
    base: str = ""
    parent: int
    children: list["Node"] = []
    edges: list[Edge] = []


class GraphBase:
    # TODO: Flesh this out a bit more
    # gravis graphs need a bit more
    # structure than just a networkx graph
    #   look in notebook around X and Y
    def __init__(self, graph=DiGraph()):
        self.graph = graph


class GraphBuilder:
    def __init__(self):
        self.graph = DiGraph()

    def add_node(self, node: Node):
        self.graph.add_node(
            node.id,
            type=node.type,
            filename=node.filename,
            label=node.label,
            parent=node.parent,
        )
        if node.parent is not None:
            self.graph.add_edge(node.parent, node.id)

    def add_edge(self, edge: Edge):
        self.graph.add_edge(edge.source, edge.target)

    def get_graph(self):
        return self.graph


class Repo:
    """The data of a file. [name, size, raw (files, folders)]"""

    def __init__(self, owner: str, repo: str, size: int, raw: dict[str, File | Folder]):
        self.owner = owner
        self.repo = repo
        self.size = size
        self.raw = raw
