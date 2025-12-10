from fastapi import FastAPI, HTTPException
from uuid import uuid4
from app.models import CreateGraphRequest, RunGraphRequest, WorkflowState, GraphDefinition
from app.engine import WorkflowEngine
from app.tools import TOOL_REGISTRY

app = FastAPI()
graphs = {}
runs = {}


@app.post("/graph/create")
def create_graph(payload: CreateGraphRequest):
    gid = str(uuid4())
    graphs[gid] = payload.definition
    return {"graph_id": gid}


from fastapi import BackgroundTasks

async def run_workflow_task(run_id: str, graph: GraphDefinition, state: dict):
    engine = WorkflowEngine(graph, tool_registry=TOOL_REGISTRY)
    final_state = await engine.run(state)
    runs[run_id] = final_state


@app.post("/graph/run")
async def run_graph(payload: RunGraphRequest, background_tasks: BackgroundTasks):
    if payload.graph_id not in graphs:
        raise HTTPException(404, "Graph not found")

    rid = str(uuid4())
    runs[rid] = WorkflowState(data=payload.initial_state, execution_log=["Queued"])

    background_tasks.add_task(
        run_workflow_task,
        rid,
        graphs[payload.graph_id],
        payload.initial_state
    )

    return {"run_id": rid, "status": "Queued"}

@app.get("/graph/state/{run_id}")
def get_state(run_id: str):
    return runs.get(run_id, {})