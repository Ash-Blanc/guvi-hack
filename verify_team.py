from app.team import get_fraud_detection_team
from app.agents.honeypot import get_honeypot_agent
import os
from dotenv import load_dotenv

load_dotenv()

def verify():
    msg = "Your account is blocked. Click http://scam.com to verify."
    
    print("\n--- Testing HoneypotAgent Isolation ---")
    honeypot = get_honeypot_agent()
    try:
        # Pass just the message to the standalone agent
        h_response = honeypot.run(msg, stream=False)
        print("Honeypot Response:")
        if hasattr(h_response, 'content'):
            print(h_response.content)
        else:
            print(h_response)
    except Exception as e:
        print(f"Honeypot Error: {e}")

    print("\n--- Testing Team Delegation ---")
    team = get_fraud_detection_team()
    print(f"Sending message: {msg}")
    
    try:
        response = team.run(msg, stream=False)
        print("\n--- Response From Team ---")
        if hasattr(response, 'content'):
            print(f"Content: {response.content}")
        else:
            print(f"Raw Response: {response}")
            
        print("\n--- Tool Calls ---")
        if hasattr(response, 'tools') and response.tools:
            print(f"Tools: {response.tools}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify()
