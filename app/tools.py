import spacy
from typing import Dict, Any

print("--- TOOLS LOADED: SPACY INTELLIGENCE ACTIVE ---")
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Spacy model not found. Run: python -m spacy download en_core_web_sm")
    nlp = None

TOOL_REGISTRY = {}

def register_tool(name: str):
    def decorator(func):
        TOOL_REGISTRY[name] = func
        return func
    return decorator

def semantic_shrink(text: str):
    words = text.split()
    while len(" ".join(words)) > 70 and len(words) > 3:
        words.pop()

    final = " ".join(words)
    if len(final) > 70:
        final = final[:67].rstrip() + "..."

    return final

def extract_subject_predicate(sentence: str):
    if not nlp:
        return sentence

    doc = nlp(sentence)

    subject = ""
    verb = ""
    complement = ""
    for token in doc:
        if token.dep_ in ("nsubj", "nsubjpass"):
            subject = " ".join(t.text for t in token.subtree)
        if token.dep_ == "ROOT":
            verb = token.text
        elif token.dep_ == "cop":
            verb = token.text
        if token.dep_ in ("attr", "acomp", "oprd", "dobj"):
            complement = " ".join(t.text for t in token.subtree)
            for child in token.head.children:
                if child.dep_ in ("prep", "acl", "advcl"):
                    complement += " " + " ".join(t.text for t in child.subtree)

    phrase = " ".join(part for part in [subject, verb, complement] if part)
    return phrase if phrase else sentence.split(",")[0]

@register_tool("split_text")
def split_text(state: Dict[str, Any]) -> Dict[str, Any]:
    text = state.get("text", "")
    chunks = [c.strip() for c in text.split('.') if len(c.strip()) > 5]
    return {
        "chunks": chunks,
        "logs": state.get("logs", []) + [f"Found {len(chunks)} sentences."]}


@register_tool("generate_lead")
def generate_lead(state: Dict[str, Any]) -> Dict[str, Any]:
    chunks = state.get("chunks", [])
    summaries = []
    logs = state.get("logs", [])
    if chunks:
        lead_sentence = chunks[0]
        smart_summary = extract_subject_predicate(lead_sentence)
        summaries.append(smart_summary)
        logs.append(f"Smart extracted: '{smart_summary}'")

    return {"summaries": summaries, "logs": logs}


@register_tool("merge_summaries")
def merge_summaries(state: Dict[str, Any]) -> Dict[str, Any]:
    summaries = state.get("summaries", [])
    merged = " ".join(summaries)

    return {
        "current_summary": merged,
        "logs": state.get("logs", []) + ["Draft prepared."] }


@register_tool("refine_summary")
def refine_summary(state: Dict[str, Any]) -> Dict[str, Any]:
    current = state.get("current_summary", "")
    limit = state.get("limit", 70)
    logs = state.get("logs", [])

    if len(current) <= limit:
        logs.append(f"Length OK: {len(current)} <= {limit}")
        return {"current_summary": current, "status": "READY", "logs": logs}

    refined = semantic_shrink(current)
    logs.append(f"Shrunk to: '{refined}'")

    return {
        "current_summary": refined,
        "status": "TOO_LONG",
        "logs": logs}