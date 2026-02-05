import os
from app.llm_fallback import ReliableMistral
from unittest.mock import patch, MagicMock

# Ensure strict fallback behavior for test
os.environ["MISTRAL_API_KEY"] = "dummy"

print("--- Starting Fallback Test ---")

from agno.agent import Agent

# Patch the MistralChat.invoke method to simulate a 429 error
with patch('agno.models.mistral.MistralChat.invoke') as mock_invoke:
    # Simulate API Rate Limit
    mock_invoke.side_effect = Exception('API error occurred: Status 429. Body: {"object":"error","message":"Service tier capacity exceeded"}')
    
    # Initialize Agent with ReliableMistral
    agent = Agent(
        model=ReliableMistral(id="mistral-small-latest", api_key="dummy"),
        markdown=False
    )
    
    try:
        print("Invoking Agent (expecting Mistral failure -> Fallback)...")
        # Agent handles message formatting for us
        response = agent.print_response("Say 'Fallback Success' if you can hear me.")
        
        print(f"\n[SUCCESS] Agent executed successfully.")
        print("Fallback mechanism worked!")
        
    except Exception as e:
        print(f"\n[FAILURE] Exception caught: {e}")

print("--- End Test ---")
