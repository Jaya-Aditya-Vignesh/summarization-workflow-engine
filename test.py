import requests
import time

BASE_URL = "http://127.0.0.1:8000"


def run_test():
    print("[*] Creating Option B Graph...")
    graph_payload = {
        "name": "Summarization Agent",
        "definition": {
            "start_node": "split",
            "nodes": [
                {"id": "split", "function_name": "split_text"},
                {"id": "gen_sum", "function_name": "generate_summaries"},
                {"id": "merge", "function_name": "merge_summaries"},
                {"id": "refine", "function_name": "refine_summary"}
            ],
            "edges": [
                {"from_node": "split", "to_node": "gen_sum"},
                {"from_node": "gen_sum", "to_node": "merge"},
                {"from_node": "merge", "to_node": "refine"},

                {
                    "from_node": "refine",
                    "to_node": "refine",
                    "condition_key": "status",
                    "condition_value": "TOO_LONG"
                },
                {
                    "from_node": "refine",
                    "to_node": None,
                    "condition_key": "status",
                    "condition_value": "READY"
                }
            ]
        }
    }

    resp = requests.post(f"{BASE_URL}/graph/create", json=graph_payload)
    graph_id = resp.json()["graph_id"]
    print(f"[+] Graph Created: {graph_id}")

    long_text = "Tredence is data science and AI company focused on the last mile of analytics, bridging the gap between raw insights and actual business value. Comapany specialize in operationalizing data for retail, CPG, and supply chain enterprises to drive faster, actionable decision-making."

    print("[*] Running Workflow...")
    run_resp = requests.post(f"{BASE_URL}/graph/run", json={
        "graph_id": graph_id,
        "initial_state": {"text": long_text, "limit": 30}
    })
    run_id = run_resp.json()["run_id"]

    # 3. Poll
    while True:
        state_resp = requests.get(f"{BASE_URL}/graph/state/{run_id}")
        data = state_resp.json()
        if "Workflow Completed" in data.get("execution_log", []):
            break
        time.sleep(0.5)

    print("\n=== FINAL SUMMARY ===")
    print(f"Original Text: {long_text}")
    print(f"Final Summary: {data['data'].get('current_summary')}")
    print(f"Final Length:  {len(data['data'].get('current_summary'))} (Limit: 30)")

    print("\n=== LOGS ===")
    for log in data['data']['logs']:
        print(f" > {log}")


if __name__ == "__main__":
    run_test()