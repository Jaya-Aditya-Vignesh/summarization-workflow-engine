import asyncio
from typing import Dict, Any, Optional, Callable
from app.models import GraphDefinition, WorkflowState


class WorkflowEngine:
    def __init__(self, definition: GraphDefinition, tool_registry: Dict[str, Callable]):
        self.nodes = {n.id: n for n in definition.nodes}
        self.edges = definition.edges
        self.start_node = definition.start_node
        self.tool_registry = tool_registry

    def get_next_node(self, current_node: str, state_data: Dict[str, Any]) -> Optional[str]:
        candidates = [e for e in self.edges if e.from_node == current_node]
        for edge in candidates:
            if edge.condition_key:
                val = state_data.get(edge.condition_key)
                if str(val) == str(edge.condition_value):
                    return edge.to_node
            else:
                return edge.to_node
        return None

    async def run(self, initial_state: Dict[str, Any]) -> WorkflowState:
        state = WorkflowState(data=initial_state)
        curr_id = self.start_node
        steps = 0

        while curr_id and steps < 20:
            node = self.nodes.get(curr_id)
            if not node: break

            state.execution_log.append(f"Step {steps}: Running {node.id}")

            func = self.tool_registry.get(node.function_name)
            if func:
                if asyncio.iscoroutinefunction(func):
                    updates = await func(state.data)
                else:
                    updates = func(state.data)
                if updates: state.data.update(updates)
            else:
                state.execution_log.append(f"ERROR: Tool '{node.function_name}' not found")

            curr_id = self.get_next_node(curr_id, state.data)
            steps += 1

        state.execution_log.append("Workflow Completed")
        return state