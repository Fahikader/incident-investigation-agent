from typing import Annotated
from pydantic import BaseModel, Field

class TimelineEvent(BaseModel):
    timestamp: Annotated[str, Field(description="The timestamp of the event, e.g., '2024-06-01 11:15:00'.")]
    service: Annotated[str, Field(description="The name of the service associated with the event.")]
    event_type: Annotated[str, Field(description="The type of event (e.g., 'log', 'metric', 'deployment', 'runbook').")]
    details: Annotated[str, Field(description="Clear description of what happened at this event.")]

class Hypothesis(BaseModel):
    hypothesis_id: Annotated[str, Field(description="A unique identifier for the hypothesis, e.g., 'H1'.")]
    description: Annotated[str, Field(description="A brief description of the root cause hypothesis.")]
    confidence_level: Annotated[float,Field(ge=0.0, le=1.0, description="A confidence level (0.0 to 1.0) indicating likelihood.")]
    supporting_evidence: Annotated[list[TimelineEvent], Field(description="Verified timeline events supporting this hypothesis.")]

class InvestigationReport(BaseModel):
    report_id: Annotated[str, Field(description="A unique identifier for the investigation report.")]
    service_name: Annotated[str, Field(description="The primary service being investigated.")]
    incident_summary: Annotated[str, Field(description="A concise summary of the incident.")]
    timeline: Annotated[list[TimelineEvent], Field(description="Chronological sequence of events during the incident.")]
    hypotheses: Annotated[list[Hypothesis], Field(description="Evidence-backed root cause hypotheses.")]
    assumptions_and_gaps: Annotated[list[str], Field(description="Explicit list of assumptions or missing data not directly proven by evidence.")]
    recommendations: Annotated[list[str], Field(description="Recommended remediation steps based on runbooks.")]

