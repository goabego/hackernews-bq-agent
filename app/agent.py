# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import google.auth
from google.adk.agents import Agent
from google.adk.tools.bigquery import BigQueryCredentialsConfig
from google.adk.tools.bigquery import BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig
from google.adk.tools.bigquery.config import WriteMode
import os

# --- Environment Setup ---
try:
    _, project_id = google.auth.default()
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
    os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
    os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")
    print(f"Using Google Cloud Project: {project_id}")
except (google.auth.exceptions.DefaultCredentialsError, TypeError):
    print("Google Cloud credentials not found. Please authenticate.")
    exit()

PROJECT_ID=project_id

# --- Tool Configuration ---

# Define a credentials config using application default credentials
# https://cloud.google.com/docs/authentication/provide-credentials-adc
application_default_credentials, _ = google.auth.default()
credentials_config = BigQueryCredentialsConfig(
    credentials=application_default_credentials
)

# Instantiate a BigQuery toolset
tool_config = BigQueryToolConfig(
    write_mode=WriteMode.ALLOWED,
)



bigquery_toolset = BigQueryToolset(
    credentials_config=credentials_config,
    bigquery_tool_config=tool_config
)

def get_current_project() -> str:
    """
    Returns the current Google Cloud project ID.
    The agent should use this tool to get the project ID for queries.
    """
    return PROJECT_ID

def get_hacker_news_table() -> str:
    """
    Returns the BigQuery Hacker News Public Table ID name to be used by the agent.
    The agent should use this tool to get the table ID for queries.
    """
    return "`bigquery-public-data.hacker_news.full`"


def get_data_schema(query: str) -> str:
    """
    Returns the schema for the Hacker News BigQuery table.
    The agent should use this tool to understand the table structure before writing a query.
    """
    return """
        The Hacker News table schema (`bigquery-public-data.hacker_news.full`) is as follows:
        - title: Story title (STRING)
        - url: Story url (STRING)
        - text: Story or comment text (STRING)
        - dead: Is dead? (BOOLEAN)
        - by: The username of the item's author (STRING)
        - score: Story score (INTEGER)
        - time: Unix time (INTEGER)
        - timestamp: Timestamp for the unix time (TIMESTAMP)
        - type: Type of details (comment, story, job, etc.) (STRING)
        - id: The item's unique id (INTEGER)
        - parent: Parent comment ID (INTEGER)
        - descendants: Number of story or poll descendants (INTEGER)
        - deleted: Is deleted? (BOOLEAN)"""


# --- Agent Definition ---

root_agent = Agent(
    name="hackernews_bigquery_agent",
    model="gemini-1.5-flash",
    description=(
        "An agent that can answer questions about the Hacker News dataset by "
        "executing SQL queries against BigQuery."
    ),
    instruction="""
        You are an expert data science agent. Your primary goal is to answer user questions
        by writing and executing SQL queries against the `bigquery-public-data.hacker_news.full` table.

        --- Querying Best Practices ---
        1.  **Ranking Stories:** When a user asks for "top", "best", or "most popular" stories, you MUST order the results by the `score` field in descending order (`ORDER BY score DESC`).
        2.  **Filter for Stories:** For any question about stories, you MUST filter the query to only include items of that type (`WHERE type = 'story'`).
        3.  **Exclude Invalid Entries:** Always add conditions to your queries to exclude dead or deleted stories (`WHERE dead IS NOT TRUE AND deleted IS NOT TRUE`).

        --- Workflow ---
        1.  First, use the `get_data_schema` tool if you are unsure about column names or data types.
        2.  Then, construct a precise SQL query that follows all the best practices above.
        3.  Finally, use the `bigquery_toolset.query_tool.execute_sql` tool to run your query and present the results clearly to the user.
    """,
    # The tool list is simplified for clarity and robustness.
    tools=[bigquery_toolset, get_data_schema],
)