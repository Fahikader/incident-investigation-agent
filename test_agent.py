from strands import Agent, tool
from strands.models import BedrockModel
from tools import query_logs, read_metrics, list_deployments, search_runbooks
from schemas import InvestigationReport
from hooks import InvestigationHook

model = BedrockModel(model_id="eu.anthropic.claude-opus-4-6-v1", region_name="eu-north-1")

def run_test(name: str, query: str, tools_list: list):
    print(f"\n=== TEST: {name} ===")
    hook = InvestigationHook(max_tool_calls=8)
    agent = Agent(model=model, tools=tools_list, hooks=[hook])
    report = agent.structured_output(InvestigationReport, query)
    print("Summary:", report.incident_summary)
    print("Assumptions/Gaps:", report.assumptions_and_gaps)
    print("Trace steps:", len(hook.trace))

if __name__ == "__main__":
    # 1. Known Incident
    run_test(
        "Known Incident (video-worker)",
        "Investigate video-worker memory leak around 2024-06-01 13:00:00",
        [query_logs, read_metrics, list_deployments, search_runbooks],
    )

    # 2. Missing Data
    run_test(
        "Missing Data (payment-api)",
        "Investigate payment-api outage",
        [query_logs, read_metrics, list_deployments, search_runbooks],
    )

    # 3. Misleading Correlation (file-service had 80% disk at 10:10, file not found at 12:45)
    run_test(
        "Misleading Correlation (file-service)",
        "Investigate file-service 'File not found' at 2024-06-01 12:45:00. Check if disk space caused it.",
        [query_logs, read_metrics, list_deployments, search_runbooks],
    )

    # 4. Tool Failure
    @tool
    def broken_logs(Service: str) -> list[dict]:
        """Search application logs for a given service name."""
        raise ConnectionError("Log database is offline")

    run_test(
        "Tool Failure",
        "Investigate auth-api login failures",
        [broken_logs, read_metrics, list_deployments, search_runbooks],
    )
