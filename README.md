Sentinels: Autonomous Regulatory Compliance Agents
Capstone Project | Enterprise Agents Track

The Sentinels project is a Level 3 Multi-Agent System designed to transform regulatory compliance from a reactive manual process into a continuous, autonomous operation. It utilizes the Google Agent Development Kit (ADK) to orchestrate a team of specialized agents that cross-reference internal corporate documents against live external regulations.

🏗 Architecture
The system utilizes the Coordinator Pattern, consisting of three agent personas:

Audit Lead (Coordinator): Manages the audit lifecycle, delegates tasks, and synthesizes the final compliance report.

Research Agent: Connects to external regulatory databases via the Model Context Protocol (MCP) to fetch authoritative legal texts.

Analyst Agent: Retrieves internal policy documents and performs gap analysis.

🚀 Setup & Usage
Prerequisites
Python 3.10+

Google Cloud Project with Vertex AI API enabled.

Gemini API Key.

Installation
**Clone the repository:**bash git clone https://github.com/your-org/sentinels.git cd sentinels


Install dependencies:

Bash
pip install -r requirements.txt
Configure Environment: Set your GOOGLE_API_KEY and GOOGLE_CLOUD_PROJECT environment variables.

Running an Audit
Execute the main script to start a compliance audit session:

Bash
python -m sentinels.main
🛠 Tech Stack
Framework: Google Agent Development Kit (ADK)

Models: Gemini 1.5 Pro (Coordinator), Gemini 1.5 Flash (Specialists)

Interoperability: Model Context Protocol (MCP)

Persistence: Vertex AI Memory Bank


### `requirements.txt`

google-adk>=0.4.0
google-genai
mcp
opentelemetry-api
opentelemetry-sdk

---

## Source Code

### `sentinels/config.py`
*Configuration for models, retry logic, and cloud resources.*

```python
import os
from google.genai import types

# Robustness Configuration: Exponential Backoff for API resilience
RETRY_CONFIG = types.HttpRetryOptions(
    attempts=5,
    exp_base=2,
    initial_delay=1,
    http_status_codes=
)

# Model Selection Strategy
# We use Flash for sub-agents to optimize cost and speed.
SUB_AGENT_MODEL = "gemini-1.5-flash" 
# We use Pro for the coordinator to maximize reasoning capabilities.
COORDINATOR_MODEL = "gemini-1.5-pro"

# Project Environment Variables
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
AGENT_ENGINE_ID = "compliance-memory-bank-prod"
