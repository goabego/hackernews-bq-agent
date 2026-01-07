# Building a BigQuery Data Agent with Google ADK

This repository serves as an educational example of how to build an **AI Agent** capable of interacting with a real-world database—specifically, the Hacker News public dataset on Google BigQuery.

Using the **Google Agent Development Kit (ADK)** and **Gemini 2.5 Flash**, this agent demonstrates the "Text-to-SQL" paradigm, where natural language questions are converted into SQL queries, executed, and the results summarized back to the user.

---

## 📚 Key Concepts

This project demonstrates several core concepts in modern AI engineering:

### 1. Agents & Tools (Function Calling)
Large Language Models (LLMs) are powerful text generators, but they can't natively access the internet or your database. **Agents** bridge this gap by using **Tools**.
-   In this project, we give the model Python functions (e.g., `execute_sql`, `get_data_schema`).
-   The model doesn't run the code itself; it outputs structured text acting as a "request" to call a function. The ADK runtime executes the Python code and feeds the result back to the model.

### 2. Dynamic Text-to-SQL
Instead of hardcoding queries, we rely on the agent to generate SQL on the fly. This allows for infinite flexibility.
-   *User:* "Show me the top stories from 2023."
-   *Agent:* Generates `SELECT ... FROM ... WHERE timestamp BETWEEN ...`

### 3. Schema Awareness
To write good SQL, a human needs to know the table names and columns. An AI is no different.
-   We provide a specific tool (`get_data_schema`) that the agent can call to "look up" the structure of the database before it tries to write a query. This significantly reduces hallucinations (e.g., guessing a column name that doesn't exist).

---

## 🏗️ Architecture

The flow of information works as follows:

1.  **User** asks a question: *"Who wrote the most commented story yesterday?"*
2.  **Agent (Gemini)** analyzes the request and decides it needs to know the table structure.
3.  **Tool Execution**: The agent calls `get_data_schema()`.
4.  **Agent** receives the schema, then formulates a SQL query.
5.  **Tool Execution**: The agent calls `execute_sql("SELECT by, descendants ...")`.
6.  **BigQuery** executes the query and returns JSON-like rows.
7.  **Agent** interprets the raw data and generates a natural language response.

---

## 🔎 Code Deep Dive

The core logic resides in `app/agent.py`. Here are the interesting parts:

### The `BigQueryToolset`
We don't need to write the low-level API calls to Google Cloud. The ADK provides a `BigQueryToolset` that wraps the connection and execution logic.

```python
bigquery_toolset = BigQueryToolset(
    credentials_config=credentials_config,
    bigquery_tool_config=tool_config
)
```

### Prompt Engineering (`instruction`)
The "brain" of the agent is shaped by the `instruction` string passed to the `Agent` constructor. Notice how we encode domain knowledge directly into the prompt:

```python
instruction="""
    ...
    --- Querying Best Practices ---
    1. Ranking Stories: ... MUST order the results by the `score` field...
    2. Filter for Stories: ... MUST filter ... (`WHERE type = 'story'`).
    3. Exclude Invalid Entries: ... (`WHERE dead IS NOT TRUE ...`).
"""
```
This ensures that when a user asks for "top stories", the agent knows exactly how to define "top" and "story" according to our specific dataset rules.

### Custom Tools
While we use the standard BigQuery toolset, we also define custom Python functions like `get_data_schema`. The docstring is crucial because the LLM reads it to understand *when* and *how* to use the tool.

```python
def get_data_schema(query: str) -> str:
    """
    Returns the schema for the Hacker News BigQuery table.
    The agent should use this tool to understand the table structure...
    """
```

---

## 🚀 Getting Started

Follow these steps to run the agent on your local machine.

### Prerequisites

1.  **Google Cloud SDK:** Install and initialize the `gcloud` command-line tool.
2.  **Python 3.12+:** Recommended to manage with `uv` or `venv`.
3.  **Permissions:** Your Google Cloud user must have **Vertex AI User** and **BigQuery User** roles.

### Installation

1.  Create and activate a virtual environment:
    ```bash
    uv venv
    source .venv/bin/activate
    ```

2.  Install dependencies:
    ```bash
    uv pip install -e .
    ```

3.  **Authentication (Critical):**
    The agent runs locally but talks to Google Cloud services. Authenticate using Application Default Credentials (ADC):
    ```bash
    gcloud auth application-default login
    ```

### Running the Agent

Start the agent's web server:

```bash
uv run adk web . --port 8501 --reload_agents
```

Open your browser to `http://127.0.0.1:8501`.

### Example Interactions to Try

*   **Exploration:** "What columns are in the table?" (Triggers `get_data_schema`)
*   **Simple Query:** "What is the top story right now?"
*   **Complex Aggregation:** "Who are the top 5 authors by total score in 2024?"
*   **Filtering:** "Find me stories about 'Rust' that have more than 100 comments."

---

## 🔮 Further Exploration

To extend your learning, try modifying `app/agent.py`:
1.  **Add a new tool:** Create a function that calculates the "virality" of a post (e.g., score divided by time) and expose it to the agent.
2.  **Change the dataset:** Point the `get_hacker_news_table` function to a different public dataset (e.g., GitHub activity) and update the schema tool.
3.  **Refine the prompt:** Try removing the "Best Practices" section from the instruction and see how the agent's performance degrades on complex queries.
