import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from strands import Agent
from strands.models import BedrockModel


from tools import query_logs, read_metrics, list_deployments, search_runbooks
from schemas import InvestigationReport
from hooks import InvestigationHook


app = FastAPI(title="Incident Investigation Agent")
SESSION_DIR = Path("sessions")
SESSION_DIR.mkdir(exist_ok=True)


SYSTEM_PROMPT = """
You are an Incident Investigation Agent.
1. Check logs, metrics, deployments, and runbooks before answering.
2. Separate VERIFIED EVIDENCE (from tools) from ASSUMPTIONS (missing data or unverified links).
3. Watch for misleading correlations: check timestamps carefully before blaming a metric or deployment.
4. If a tool fails or returns no data, state that clearly in assumptions_and_gaps.
"""


model = BedrockModel(
    model_id="eu.anthropic.claude-opus-4-6-v1",
    region_name="eu-north-1",
)



class InvestigateRequest(BaseModel):
    session_id: str
    query: str


def load_session(session_id: str) -> list:
    file = SESSION_DIR / f"{session_id}.json"
    if file.exists():
        return json.loads(file.read_text())
    return []

def save_session(session_id: str, messages: list):
    file = SESSION_DIR / f"{session_id}.json"
    file.write_text(json.dumps(messages, default=str, indent=2))


@app.post("/investigate")
def investigate(req: InvestigateRequest):
    
    history = load_session(req.session_id)

    if len(history) >= 20:
        raise HTTPException(status_code=429, detail="Session usage limit reached.")

    
    hook = InvestigationHook(max_tool_calls=8)

   
    agent = Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[query_logs, read_metrics, list_deployments, search_runbooks],
        messages=history,
        hooks=[hook],
    )

    try:
        
        report = agent.structured_output(InvestigationReport, req.query)
    except RuntimeError as e:
        raise HTTPException(status_code=429, detail=str(e))

   
    save_session(req.session_id, agent.messages)

    return {
        "session_id": req.session_id,
        "report": report,
        "execution_trace": hook.trace,
        "tool_calls_used": hook.calls,
    }
