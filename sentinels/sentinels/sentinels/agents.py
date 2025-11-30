from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool, google_search
from.config import SUB_AGENT_MODEL, COORDINATOR_MODEL, RETRY_CONFIG
from.tools import fetch_internal_policy, flag_compliance_risk
# from.mcp_config import configure_regulatory_mcp # Uncomment if MCP server is installed

# 1. Research Agent: The External Expert
research_agent = LlmAgent(
    name="ResearchAgent",
    model=Gemini(model=SUB_AGENT_MODEL, retry_options=RETRY_CONFIG),
    instruction="""
    You are a Senior Legal Researcher. Your sole responsibility is to find and quote external regulations.
    1. Use 'google_search' for broad context.
    2. Always cite your sources. Do not interpret the law; quote it verbatim.
    """,
    # In a real environment, include configure_regulatory_mcp() in this list
    tools=[google_search], 
    output_key="external_legal_context"
)

# 2. Analyst Agent: The Internal Investigator
analyst_agent = LlmAgent(
    name="AnalystAgent",
    model=Gemini(model=SUB_AGENT_MODEL, retry_options=RETRY_CONFIG),
    instruction="""
    You are a Compliance Auditor. Your job is to verify if our internal policies match external requirements.
    1. You will receive legal context from the Research Agent.
    2. Use 'fetch_internal_policy' to retrieve the relevant company documents.
    3. Compare the internal text against the external legal text.
    4. If a gap is found, use 'flag_compliance_risk' to report it.
    """,
    tools=[fetch_internal_policy, flag_compliance_risk],
    output_key="audit_results"
)

# 3. Audit Lead: The Coordinator
coordinator_agent = LlmAgent(
    name="AuditLead",
    model=Gemini(model=COORDINATOR_MODEL, retry_options=RETRY_CONFIG),
    instruction="""
    You are the Chief Compliance Officer. You are responsible for the entire audit lifecycle.
    
    EXECUTION PLAN:
    1. PLAN: Analyze the user's request to identify which regulations and internal policies are involved.
    2. RESEARCH: Delegate to 'ResearchAgent' to retrieve the specific external laws.
    3. AUDIT: Delegate to 'AnalystAgent' to check our internal documents against those laws.
    4. REPORT: Synthesize the findings into a final, actionable report.
    
    You must coordinate the sub-agents effectively.
    """,
    tools=
)
