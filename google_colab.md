3. Google Colab Notebook
To run this project immediately in Google Colab, create a new notebook and paste the following into the first cell to setup the environment and write the files to the filesystem.

Python
# Cell 1: Install Dependencies
!pip install google-adk google-genai

# Cell 2: Authenticate (Colab Only)
from google.colab import userdata
import os

# Ensure you have added 'GOOGLE_API_KEY' to your Colab secrets
os.environ = userdata.get('GOOGLE_API_KEY')
os.environ = "your-project-id" # Optional if using Gemini API only

# Cell 3: Create Package Structure
!mkdir -p sentinels
!touch sentinels/__init__.py

# Cell 4: Write Config File
%%writefile sentinels/config.py
import os
from google.genai import types

RETRY_CONFIG = types.HttpRetryOptions(attempts=3, exp_base=2, initial_delay=1, http_status_codes=)
SUB_AGENT_MODEL = "gemini-1.5-flash"
COORDINATOR_MODEL = "gemini-1.5-pro"

# Cell 5: Write Tools File
%%writefile sentinels/tools.py
from typing import Dict
from google.adk.tools import ToolContext

INTERNAL_POLICIES = {
    "data_retention": "All customer data must be retained for 5 years. Deletion requests processed in 30 days.",
    "access_control": "Multi-factor authentication is required for all production databases."
}

def fetch_internal_policy(policy_id: str, context: ToolContext) -> Dict[str, str]:
    """Retrieves internal policy text."""
    print(f" Accessing policy: {policy_id}")
    return {"status": "success", "content": INTERNAL_POLICIES.get(policy_id.lower(), "Not found")}

def flag_compliance_risk(risk_level: str, description: str, context: ToolContext) -> Dict[str, str]:
    """Flags a compliance risk."""
    print(f" RISK FLAGGED: {risk_level}")
    return {"status": "escalated", "ticket_id": "12345"}

# Cell 6: Write Agents File
%%writefile sentinels/agents.py
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool, google_search
from.config import SUB_AGENT_MODEL, COORDINATOR_MODEL, RETRY_CONFIG
from.tools import fetch_internal_policy, flag_compliance_risk

research_agent = LlmAgent(
    name="ResearchAgent",
    model=Gemini(model=SUB_AGENT_MODEL, retry_options=RETRY_CONFIG),
    instruction="Find external regulations using google_search. Cite sources.",
    tools=[google_search],
    output_key="legal_context"
)

analyst_agent = LlmAgent(
    name="AnalystAgent",
    model=Gemini(model=SUB_AGENT_MODEL, retry_options=RETRY_CONFIG),
    instruction="Compare external laws (from context) with internal policies using fetch_internal_policy.",
    tools=[fetch_internal_policy, flag_compliance_risk],
    output_key="audit_results"
)

coordinator_agent = LlmAgent(
    name="AuditLead",
    model=Gemini(model=COORDINATOR_MODEL, retry_options=RETRY_CONFIG),
    instruction="Coordinate the audit. 1. Research laws. 2. Check internal policies. 3. Report.",
    tools=
)

# Cell 7: Run Application
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from sentinels.agents import coordinator_agent

async def main():
    runner = Runner(agent=coordinator_agent, session_service=InMemorySessionService())
    query = "Audit our 'data_retention' policy against GDPR standards."
    print(f"Starting: {query}")
    
    response = await runner.run_debug(query)
    print("\nFinal Response:\n", response.content.parts.text)

await main()
