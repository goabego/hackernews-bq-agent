# BigQuery Hacker News Agent

This project contains a sophisticated AI agent built with the Google Agent Development Kit (ADK). The agent is designed to answer natural language questions about the public Hacker News dataset by intelligently constructing and executing SQL queries against Google BigQuery.

## Features

-   **Natural Language Queries:** Ask questions in plain English (e.g., "What are the top stories from the last week?").
-   **Dynamic SQL Generation:** The agent writes its own SQL queries based on your questions.
-   **Direct BigQuery Integration:** Uses a pre-configured BigQuery toolset to interact directly with Google Cloud.
-   **Schema Aware:** Includes a tool that allows the agent to inspect the table schema to write more accurate queries.

---

## Setup and Initialization

### Prerequisites

1.  **Google Cloud SDK:** You must have the `gcloud` command-line tool installed and initialized.
2.  **Python Environment:** A working Python environment (like the one managed by `uv` in this project).
3.  **Permissions:** The Google Cloud user or service account running the agent must have the **"Vertex AI User"** (`roles/aiplatform.user`) and **"BigQuery User"** (`roles/bigquery.user`) roles on the target Google Cloud project.

### Local Development Authentication

When running this agent on your local machine (outside of Google Cloud Shell), you must authenticate your environment using Application Default Credentials (ADC). This is a critical step that allows the agent to securely access Google Cloud services on your behalf.

Run the following command in your terminal and follow the browser-based authentication flow:

```bash
gcloud auth application-default login
```

This command saves a credential file on your local system that the ADK and Google Cloud client libraries will automatically detect and use for authentication.

---

## Running the Agent

Once your environment is authenticated, you can start the agent's web server using the following command:

```bash
uv run adk web . --port 8501 --reload_agents
```

This will start a local web server, and you can interact with your agent through the web UI provided by the ADK.

## How to Use the Tool

After starting the server, open your web browser to the local address (e.g., `http://127.0.0.1:8501`) and ask the agent questions. The agent understands the context of the Hacker News dataset.

### Example Questions:

-   "What is the top story on Hacker News right now?"
-   "Show me the top 5 stories from the last 7 days."
-   "What were the most popular stories about 'Go-to-Market' last month?"
-   "Who are the top 10 authors by total story score?"

### Example 
User: Get the top 5 post in the last month.

Response: 

Here are the top 5 Hacker News posts from the last month:

Title: AWS multiple services outage in us-east-1
URL: https://health.aws.amazon.com/health/status?ts=20251020
Score: 2241
Timestamp: 2025-10-20 07:22:28+00:00

Title: A WebGL game where you deliver messages on a tiny planet
URL: https://messenger.abeto.co/
Score: 2131
Timestamp: 2025-09-27 15:17:30+00:00

Title: Fire destroys S. Korean government's cloud storage system, no backups available
URL: https://koreajoongangdaily.joins.com/news/2025-10-01/national/socialAffairs/NIRS-fire-destroys-governments-cloud-storage-system-no-backups-available/2412936
Score: 2080
Timestamp: 2025-10-05 17:20:39+00:00

Title: Space Elevator
URL: https://neal.fun/space-elevator/
Score: 1783
Timestamp: 2025-10-20 04:42:08+00:00

Title: How I bypassed Amazon's Kindle web DRM
URL: https://blog.pixelmelt.dev/kindle-web-drm/
Score: 1756
Timestamp: 2025-10-16 20:22:48+00:00