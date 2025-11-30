import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.apps.app import App, EventsCompactionConfig
from.agents import coordinator_agent

# Session Service: Manages conversation history
session_service = InMemorySessionService()

# Application Container with Context Compaction
compliance_app = App(
    name="ComplianceSentinels",
    root_agent=coordinator_agent,
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=5, 
        overlap_size=2         
    )
)

async def run_compliance_audit(query: str):
    """
    Executes the main audit workflow.
    """
    runner = Runner(
        app=compliance_app,
        session_service=session_service
    )
    
    session_id = "audit-session-001"
    print(f"--- Initiating Compliance Audit: {query} ---")
    
    async for event in runner.run_async(
        user_id="chief_auditor",
        session_id=session_id,
        new_message=query
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.function_call:
                    print(f" > [Orchestrator] Delegating to: {part.function_call.name}")
                if part.text and not event.is_final_response():
                    print(f" > {part.text[:80]}...")
        
        if event.is_final_response():
            print(f"\n--- Final Audit Report ---\n{event.content.parts.text}")

if __name__ == "__main__":
    # Example execution
    asyncio.run(run_compliance_audit(
        "Audit our internal 'data_retention' policy against standard GDPR requirements."
    ))
