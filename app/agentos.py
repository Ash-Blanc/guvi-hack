from dotenv import load_dotenv
load_dotenv()

from agno.os import AgentOS
from agno.db.sqlite import SqliteDb
from app.agent import get_honeypot_agent

# Initialize the agent with database storage for persistence
# Using SqliteDb as per updated Agno patterns
db = SqliteDb(session_table="agent_sessions", db_file="agent_storage.db")
agent = get_honeypot_agent(db=db)

# Initialize AgentOS with the agent
agent_os = AgentOS(agents=[agent])

# Get the FastAPI app
app = agent_os.get_app()

if __name__ == "__main__":
    # Serve the application
    # Note: Use 'app.agentos:app' string for reload support
    agent_os.serve(app="app.agentos:app", reload=True)
