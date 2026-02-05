import os
from fastapi import FastAPI, Header, HTTPException, Request
from .models import APIRequest, APIResponse, FinalCallbackPayload, ExtractedIntelligence
from .agent import process_message
from .intelligence import extract_intelligence, is_scam
import httpx
from dotenv import load_dotenv
from typing import Dict, Set

load_dotenv()

app = FastAPI(title="Agentic Honey-Pot API")

# Mock API Key for demo purposes
EXPECTED_API_KEY = os.getenv("API_KEY", "test-key")
GUVI_EVALUATION_ENDPOINT = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

# Local file mode (for testing - writes to file instead of POST callback)
LOCAL_FILE_MODE = os.getenv("LOCAL_FILE_MODE", "false").lower() == "true"
INTEL_OUTPUT_DIR = "intelligence_reports"

# =============================================================================
# SESSION TRACKING FOR SMART CALLBACKS
# =============================================================================

# In-memory session store (use Redis/DB in production)
_session_intel: Dict[str, ExtractedIntelligence] = {}
_reported_sessions: Set[str] = set()

# Thresholds for triggering callback
MIN_TURNS_FOR_CALLBACK = 3  # Minimum turns before callback
HIGH_VALUE_INTEL_IMMEDIATE = True  # Callback immediately if high-value intel found


def _merge_intel(existing: ExtractedIntelligence, new: ExtractedIntelligence) -> ExtractedIntelligence:
    """Merge new intelligence into existing accumulated intel."""
    return ExtractedIntelligence(
        bankAccounts=list(set(existing.bankAccounts + new.bankAccounts)),
        upiIds=list(set(existing.upiIds + new.upiIds)),
        phishingLinks=list(set(existing.phishingLinks + new.phishingLinks)),
        phoneNumbers=list(set(existing.phoneNumbers + new.phoneNumbers)),
        suspiciousKeywords=list(set(existing.suspiciousKeywords + new.suspiciousKeywords)),
    )


def _has_high_value_intel(intel: ExtractedIntelligence) -> bool:
    """Check if we have high-value intel worth reporting."""
    return bool(intel.bankAccounts or intel.upiIds or intel.phishingLinks)


def _should_trigger_callback(session_id: str, total_turns: int, intel: ExtractedIntelligence) -> bool:
    """
    Determine if callback should be triggered.
    
    Rules:
    1. Never trigger if already reported for this session
    2. Trigger immediately if high-value intel (bank/UPI/phishing) found
    3. Otherwise, wait for MIN_TURNS_FOR_CALLBACK turns with confirmed scam
    """
    # Already reported - don't spam
    if session_id in _reported_sessions:
        return False
    
    # High-value intel = immediate trigger
    if HIGH_VALUE_INTEL_IMMEDIATE and _has_high_value_intel(intel):
        return True
    
    # Minimum engagement threshold met + has any intel
    if total_turns >= MIN_TURNS_FOR_CALLBACK:
        has_any_intel = intel.phoneNumbers or intel.suspiciousKeywords
        return has_any_intel
    
    return False


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.post("/analyze", response_model=APIResponse)
async def analyze(request: APIRequest, x_api_key: str = Header(None)):
    if x_api_key != EXPECTED_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
    session_id = request.sessionId
    total_turns = len(request.conversationHistory) + 1
    
    # Process the message through the agent
    response = await process_message(request)
    
    # Extract intelligence from ALL messages in conversation
    all_text = request.message.text
    for msg in request.conversationHistory:
        all_text += " " + msg.text
    
    new_intel = extract_intelligence(all_text)
    
    # Accumulate intel for this session
    if session_id in _session_intel:
        accumulated = _merge_intel(_session_intel[session_id], new_intel)
    else:
        accumulated = new_intel
    _session_intel[session_id] = accumulated
    
    # Check if we should trigger callback
    if is_scam(request.message.text, new_intel):
        if _should_trigger_callback(session_id, total_turns, accumulated):
            await trigger_callback(request, accumulated, total_turns)
            _reported_sessions.add(session_id)  # Mark as reported
        else:
            print(f"Session {session_id}: Scam detected but waiting for more engagement (turn {total_turns}/{MIN_TURNS_FOR_CALLBACK})")
    
    return response


async def trigger_callback(request: APIRequest, intel: ExtractedIntelligence, total_turns: int):
    """Send callback with accumulated intelligence or write to local file."""
    # Build agent notes based on what was extracted
    notes_parts = []
    if intel.upiIds:
        notes_parts.append(f"UPI IDs extracted: {intel.upiIds}")
    if intel.bankAccounts:
        notes_parts.append(f"Bank accounts: {intel.bankAccounts}")
    if intel.phishingLinks:
        notes_parts.append(f"Phishing links: {intel.phishingLinks}")
    if intel.phoneNumbers:
        notes_parts.append(f"Phone numbers: {intel.phoneNumbers}")
    
    agent_notes = "Scam confirmed after sufficient engagement. " + "; ".join(notes_parts) if notes_parts else "Scam detected via pattern analysis."
    
    payload = FinalCallbackPayload(
        sessionId=request.sessionId,
        scamDetected=True,
        totalMessagesExchanged=total_turns,
        extractedIntelligence=intel,
        agentNotes=agent_notes
    )
    
    # LOCAL FILE MODE - Write to file instead of POST
    if LOCAL_FILE_MODE:
        os.makedirs(INTEL_OUTPUT_DIR, exist_ok=True)
        output_file = os.path.join(INTEL_OUTPUT_DIR, f"intel_{request.sessionId}.json")
        
        with open(output_file, "w") as f:
            import json
            f.write(json.dumps(payload.model_dump(), indent=2))
        
        print(f"[LOCAL FILE MODE] Session {request.sessionId}: Intelligence written to {output_file}")
        print(f"  Turns: {total_turns}, Intel: {notes_parts}")
        return
    
    # NORMAL MODE - POST to callback endpoint
    async with httpx.AsyncClient() as client:
        try:
            print(f"[CALLBACK] Session {request.sessionId}: Triggering after {total_turns} turns with intel: {notes_parts}")
            await client.post(GUVI_EVALUATION_ENDPOINT, json=payload.model_dump(), timeout=5)
        except Exception as e:
            print(f"Callback failed: {e}")


@app.get("/health")
async def health():
    return {"status": "healthy"}
