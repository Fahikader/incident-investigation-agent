# Incident Investigation Agent

An automated AI incident response agent built with **Python**, **FastAPI**, **Strands Agents SDK**, **Pydantic**, and **Amazon Bedrock (Claude Opus)**.

## Features
- **Multi-Source Investigation:** Queries application logs, server metrics, deployment history, and troubleshooting runbooks via Strands `@tool` functions.
- **Evidence vs. Assumptions:** Enforces structured Pydantic outputs (`InvestigationReport`) separating verified timeline evidence from unconfirmed assumptions and data gaps.
- **Persistent Sessions:** Stores investigation conversation history by `session_id` for multi-turn follow-ups.
- **Execution Tracing & Guardrails:** Uses custom Strands `HookProvider` callbacks to log step-by-step tool traces and enforce tool-call limits.

## Quick Start
```bash
pip install fastapi uvicorn strands-agents boto3 pydantic
uvicorn main:app --reload
```
Open `http://127.0.0` to run an investigation, or execute `python test_agent.py` to run the evaluation suite.
