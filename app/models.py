from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class WorkflowState(BaseModel):
    data: Dict[str, Any] = Field(default_factory=dict)
    execution_log: List[str] = Field(default_factory=list)

class Node(BaseModel):
    id: str
    function_name: str

class Edge(BaseModel):
    from_node: str
    to_node: Optional[str] = None
    condition_key: Optional[str] = None
    condition_value: Optional[Any] = None

class GraphDefinition(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
    start_node: str

class CreateGraphRequest(BaseModel):
    name: str
    definition: GraphDefinition

class RunGraphRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]