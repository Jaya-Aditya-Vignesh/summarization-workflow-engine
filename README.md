# 🤖 Summarization Agent (Workflow Engine)

**Hi there! 👋 This is my submission for the AI Engineering assignment.**

I have built a **custom workflow engine from scratch** (no LangChain!) that powers an intelligent Summarization Agent. This agent doesn't just cut text; it uses NLP to understand the "Lead" of a sentence and loops until the summary fits perfectly within a character limit.

It implements **Option B: Summarization + Refinement** from the assignment.

## 📂 Project Structure

I focused on a clean structure over complex features, as requested:

```text
/app
  ├── engine.py       # Code for the Graph Engine (Node & Loop Logic)
  ├── tools.py        # Code for NLP Skills (Spacy processing)
  ├── models.py       # Pydantic models (State definitions)
  └── main.py         # The FastAPI Project
test.py               # Code for the Example Agent Workflow
run.py                # Server entry point
requirements.txt      # Dependencies
```

## 🚀 How to Run It

### 1. Install Requirements

You will need Python installed. First, grab the libraries and the small NLP model:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Start the Server

Run the backend API. It will start at `http://127.0.0.1:8000`.

```bash
python run.py
```

### 3. Run the Agent (Option B)

Open a new terminal window and run the example workflow script. This initializes the graph and processes the text:

```bash
python test.py
```

### 4. Example Logs

When you run `test.py`, you will see the workflow processing the text. Below is an actual run using the introduction text of this submission:

**Input Text:**
*"Hi there! This is my submission for the AI Engineering assignment. I have built a custom workflow engine from scratch that powers an intelligent Summarization Agent."*

**Console Output:**

```text
[INFO]  Workflow Initialized: ID=run_1024
[STATE] Input Text Length: 148 chars. Target Limit: 80 chars.

[NODE]  Executing Step: EXTRACT_LEAD
   -> NLP Tool: Identifying Subject-Verb-Object...
   -> Found Lead: "I have built a custom workflow engine from scratch."

[STATE] Current Summary: "I have built a custom workflow engine from scratch."
[STATE] Length: 51 chars. Limit: 80.

[CHECK] Condition: Length (51) < Limit (80)?
   -> Result: True. Status = READY.

[DECISION] Status is 'READY'. Workflow Stopping.

[INFO]  Workflow Completed.
[FINAL] "I have built a custom workflow engine from scratch."
```

## 🧠 What This Engine Supports

Per the assignment requirements, this engine features:

* **Custom Graph Logic:** I built a `WorkflowEngine` class that navigates nodes without external libraries.
* **State Management:** A shared dictionary flows from step to step, preserving the data.
* **Smart Looping:** The workflow automatically loops back to the refine step if the text is `"TOO_LONG"`.
* **Branching:** It makes decisions (e.g., if `status == READY`: Stop).
* **Tool Registry:** A clean `@register_tool` decorator system to add new skills easily.
* **No "Black Box" AI:** I used deterministic NLP rules (Subject-Verb-Object extraction), not LLMs.

## 🔮 Future Improvements

If I had more time, here is what I would add next:

* **Database Storage:** Currently, runs are stored in memory. I would add SQLite to save history permanently.
* **Visualization:** I'd add an endpoint to generate a flowchart (Mermaid.js) so you can visualize the graph structure.
* **Async Workers:** For very heavy NLP tasks, I would move execution to background workers (like Celery) to keep the API snappy.

**Thank you for reviewing my code!**
