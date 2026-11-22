from strands import tool

LOGS = [
    {"Incident_ID": "INC001", "Service": "auth-api", "Description": "User login failed", "Timestamp": "2024-06-01 10:15:00"},
    {"Incident_ID": "INC002", "Service": "order-api", "Description": "Database connection error", "Timestamp": "2024-06-01 11:30:00"},
    {"Incident_ID": "INC003", "Service": "file-service", "Description": "File not found", "Timestamp": "2024-06-01 12:45:00"},
    {"Incident_ID": "INC004", "Service": "video-worker", "Description": "Memory leak detected", "Timestamp": "2024-06-01 13:00:00"},
    {"Incident_ID": "INC005", "Service": "auth-api", "Description": "Unauthorized access attempt", "Timestamp": "2024-06-01 14:15:00"},
]

METRICS = [
    {"Metric_ID": "MET001", "Service": "video-worker", "Name": "CPU Usage", "Value": 75, "Timestamp": "2024-06-01 10:00:00"},
    {"Metric_ID": "MET002", "Service": "video-worker", "Name": "Memory Usage", "Value": 94, "Timestamp": "2024-06-01 13:02:00"},
    {"Metric_ID": "MET003", "Service": "file-service", "Name": "Disk Space", "Value": 80, "Timestamp": "2024-06-01 10:10:00"},
    {"Metric_ID": "MET004", "Service": "order-api", "Name": "Network Latency", "Value": 1200, "Timestamp": "2024-06-01 11:31:00"},
    {"Metric_ID": "MET005", "Service": "order-api", "Name": "Error Rate", "Value": 45, "Timestamp": "2024-06-01 11:32:00"},
]

DEPLOYMENT = [
    {"Deployment_ID": "DEP001", "Service": "auth-api", "Version": "1.0.0", "Status": "Success", "Change": "Initial release", "Timestamp": "2024-06-01 09:00:00"},
    {"Deployment_ID": "DEP002", "Service": "auth-api", "Version": "1.1.0", "Status": "Failed", "Change": "Updated OAuth token parser", "Timestamp": "2024-06-01 10:00:00"},
    {"Deployment_ID": "DEP003", "Service": "order-api", "Version": "1.2.0", "Status": "Success", "Change": "Changed database host config", "Timestamp": "2024-06-01 11:15:00"},
    {"Deployment_ID": "DEP004", "Service": "file-service", "Version": "1.3.0", "Status": "Success", "Change": "Added PDF upload support", "Timestamp": "2024-06-01 12:00:00"},
    {"Deployment_ID": "DEP005", "Service": "video-worker", "Version": "1.4.0", "Status": "Success", "Change": "Disabled frame buffer cleanup", "Timestamp": "2024-06-01 12:50:00"},
]

RUNBOOKS = [
    {"Runbook_ID": "RB001", "Title": "Restart Web Server", "Steps": ["Stop the web server", "Clear cache", "Start the web server"]},
    {"Runbook_ID": "RB002", "Title": "Database Connection Recovery", "Steps": ["Verify database host config", "Roll back recent DB config deployment", "Restart database connection pool"]},
    {"Runbook_ID": "RB003", "Title": "Memory Leak Mitigation", "Steps": ["Identify the process", "Restart the process", "Monitor memory usage"]},
    {"Runbook_ID": "RB004", "Title": "Network Latency Troubleshooting", "Steps": ["Check network cables", "Restart network devices", "Run latency tests"]},
    {"Runbook_ID": "RB005", "Title": "Unauthorized Access Response", "Steps": ["Collect error logs", "Block suspicious IP addresses", "Rotate API keys"]},
]

@tool
def query_logs(Service: str, start_time: str | None = None, end_time: str | None = None) -> list[dict]:
    """Search application logs for a given service name."""
    results = []
    for logs in LOGS:
        if logs["Service"].lower() == Service.lower():
            if start_time and logs["Timestamp"] < start_time:
                continue
            if end_time and logs["Timestamp"] > end_time:
                continue
            results.append(logs)
    if not results:
        return [{"message": f"No logs found for service '{Service}'."}]
    return results

@tool
def read_metrics(Service: str, start_time: str | None = None, end_time: str | None = None) -> list[dict]:
    """Read server health metrics such as CPU, memory, latency, and error rate for a service."""
    results = []
    for metrics in METRICS:
        if metrics["Service"].lower() == Service.lower():
            if start_time and metrics["Timestamp"] < start_time:
                continue
            if end_time and metrics["Timestamp"] > end_time:
                continue
            results.append(metrics)
    if not results:
        return [{"message": f"No metrics found for service '{Service}'."}]
    return results

@tool
def list_deployments(Service: str, start_time: str | None = None, end_time: str | None = None) -> list[dict]:
    """List recent code or configuration deployments for a service."""
    results = []
    for deployment in DEPLOYMENT:
        if deployment["Service"].lower() == Service.lower():
            if start_time and deployment["Timestamp"] < start_time:
                continue
            if end_time and deployment["Timestamp"] > end_time:
                continue
            results.append(deployment)
    if not results:
        return [{"message": f"No deployments found for service '{Service}'."}]
    return results

@tool
def search_runbooks(Title: str) -> list[dict]:
    """Search troubleshooting runbooks by keyword or issue title."""
    keywords = Title.lower().split()
    results = []
    for runbook in RUNBOOKS:
        text = (runbook["Title"] + " " + " ".join(runbook["Steps"])).lower()
        if any(word in text for word in keywords):
            results.append(runbook)
    if not results:
        return [{"message": f"No runbooks found matching '{Title}'."}]
    return results



