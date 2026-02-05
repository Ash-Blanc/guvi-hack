from datetime import datetime
import json
from .models import APIRequest, APIResponse
from .team import get_fraud_detection_team
from .intelligence import extract_intelligence, is_scam


async def process_message(request: APIRequest) -> APIResponse:
    """
    Process an incoming message through the fraud detection team.
    
    The team will:
    1. Analyze the message for scam indicators
    2. If scam detected, delegate to HoneypotAgent with appropriate persona
    3. Return a human-like response that doesn't reveal AI nature
    """
    text = request.message.text
    history_text = "\n".join([f"{m.sender}: {m.text}" for m in request.conversationHistory])
    
    # Determine first message for persona selection
    # If no history, this is the first message
    first_message = text if not request.conversationHistory else request.conversationHistory[0].text
    
    # Quick Local Intelligence Check (useful for logging/metrics)
    extracted_local = extract_intelligence(text)
    
    # Initialize the Team with first message for persona selection
    team_leader = get_fraud_detection_team(first_message=first_message)
    
    # Construct the Team Query
    query = f"""
    Incoming Message from User: "{text}"
    Sender: {request.message.sender}
    Context/History:
    {history_text}
    
    Metadata: {request.metadata}
    
    Decide if this is a scam. If yes, let the Honeypot handle it. If no, reply yourself.
    """
    
    # Run the Team asynchronously
    response = await team_leader.arun(query)
    
    reply = "No response"
    if response and response.content:
         reply = str(response.content)

    return APIResponse(status="success", reply=reply)
