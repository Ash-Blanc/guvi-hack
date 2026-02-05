import os
from fastapi import FastAPI, Header, HTTPException, Request
from .models import APIRequest, APIResponse, FinalCallbackPayload
from .agent import process_message, get_honeypot_agent
from .intelligence import extract_intelligence, is_scam
import httpx
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Agentic Honey-Pot API")

# Mock API Key for demo purposes
EXPECTED_API_KEY = os.getenv("API_KEY", "test-key")
GUVI_EVALUATION_ENDPOINT = "https://evaluation-api.guvi.ai/scam-detection/callback"

@app.post("/analyze", response_model=APIResponse)
async def analyze(request: APIRequest, x_api_key: str = Header(None)):
    if x_api_key != EXPECTED_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
    # Process the message
    response = await process_message(request)
    
    # Check if we should trigger the callback
    # For the hackathon, we trigger the callback when intelligence is extracted
    extracted = extract_intelligence(request.message.text)
    if is_scam(request.message.text, extracted):
        await trigger_callback(request, extracted)
        
    return response

async def trigger_callback(request: APIRequest, extracted):
    async with httpx.AsyncClient() as client:
        payload = FinalCallbackPayload(
            sessionId=request.sessionId,
            scamDetected=True,
            totalMessagesExchanged=len(request.conversationHistory) + 1,
            extractedIntelligence=extracted,
            agentNotes="Scam detected and intelligence extracted automatically."
        )
        try:
            # We don't wait for the callback in the main response to keep the API fast
            # but we log it
            print(f"Triggering callback to {GUVI_EVALUATION_ENDPOINT} for session {request.sessionId}")
            # await client.post(GUVI_EVALUATION_ENDPOINT, json=payload.dict())
        except Exception as e:
            print(f"Callback failed: {e}")

@app.get("/health")
async def health():
    return {"status": "healthy"}
