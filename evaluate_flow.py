import asyncio
import os
import uuid
import time
from app.models import APIRequest, Message, Metadata
from app.agent import process_message
from app.simulation.scammer_simulator import get_scammer_simulator_agent
from app.intelligence import extract_intelligence
from dotenv import load_dotenv

load_dotenv()

async def run_evaluation_session(session_id: str, max_turns: int = 5):
    print(f"--- Starting Evaluation Session: {session_id} ---")
    
    scammer_agent = get_scammer_simulator_agent()
    history = []
    
    # 1. Scammer starts
    scammer_input = "Start a new conversation with a victim. You are pretending to be from Axis Bank regarding KYC update."
    scammer_msg_response = scammer_agent.run(scammer_input)
    current_scam_text = scammer_msg_response.content
    
    print(f"\n[Scammer]: {current_scam_text}")
    
    for turn in range(max_turns):
        # 2. Prepare Request for our API
        request = APIRequest(
            sessionId=session_id,
            message=Message(
                sender="scammer",
                text=current_scam_text,
                timestamp=int(time.time() * 1000)
            ),
            conversationHistory=history,
            metadata=Metadata(channel="SMS", language="English", locale="IN")
        )
        
        # 3. System Process
        try:
            response = await process_message(request)
            honeypot_reply = response.reply
        except Exception as e:
            print(f"System Error: {e}")
            break
            
        print(f"[Honeypot]: {honeypot_reply}")
        
        # Update History
        history.append(request.message)
        history.append(Message(sender="user", text=honeypot_reply, timestamp=int(time.time() * 1000)))
        
        # 4. Check Intelligence Extraction (Simulated 'Callback' check)
        # We can perform a check here to see what the system *would* have extracted
        extracted = extract_intelligence(current_scam_text + " " + honeypot_reply) 
        # Note: Ideally we check the system's internal state, but for black-box eval we check if the conversation *contained* info
        print(f"   > Intelligence in this turn: {extracted}")

        # 5. Scammer Reacts
        scammer_query = f"""
        The victim replied: "{honeypot_reply}"
        
        Continue your scam attempt. Respond back to them.
        """
        scammer_msg_response = scammer_agent.run(scammer_query)
        current_scam_text = scammer_msg_response.content
        print(f"\n[Scammer]: {current_scam_text}")
        
    print(f"--- Session Finished ---")

if __name__ == "__main__":
    session_id = str(uuid.uuid4())
    asyncio.run(run_evaluation_session(session_id))
