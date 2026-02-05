from dotenv import load_dotenv
load_dotenv()

from agno.os import AgentOS
from agno.db.sqlite import SqliteDb
from app.team import get_fraud_detection_team

# Initialize the agent with database storage for persistence
db = SqliteDb(session_table="agent_sessions", db_file="agent_storage.db")

# Initialize the Fraud Detection Team
fraud_team = get_fraud_detection_team(db=db)

# Initialize AgentOS with the Team
agent_os = AgentOS(teams=[fraud_team])

# Get the FastAPI app
app = agent_os.get_app()

if __name__ == "__main__":
    # Serve the application
    # Note: AgentOS.serve isn't a method in the class we viewed, 
    # but the previous file had it. Let's assume the user runs via `uv run -m app.agentos`
    # which likely uses uvicorn internally or relies on `app` being exposed.
    # The previous code had `agent_os.serve` but the `AgentOS` class definition I saw didn't possess a `serve` method.
    # However, `agno` might accept `uv run -m app.agentos` if it invokes uvicorn on `app`.
    # Let's keep the user's previous pattern if it worked, or just expose `app`.
    # The previous code commanded `uv run -m app.agentos`.
    import uvicorn
    uvicorn.run("app.agentos:app", host="0.0.0.0", port=8000, reload=True)
