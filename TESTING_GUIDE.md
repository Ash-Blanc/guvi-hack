# End-to-End API Testing Guide

This guide explains how to test the Honeypot API with realistic multi-turn conversations.

## Quick Start

### 1. Start the API Server (with local file mode)

```bash
# Enable local file mode to save intelligence to files instead of POST callback
export LOCAL_FILE_MODE=true
uv run uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### 2. Run the Multi-Turn Test

```bash
./test_conversation.sh
```

This will:
- Simulate a 7-turn GST scam conversation
- Show each turn and agent response in terminal
- Save conversation log to `test_results_<session_id>.txt`
- Save extracted intelligence to `intelligence_reports/intel_<session_id>.json`

---

## Test Scenarios

### Scenario 1: GST/Business Scam (Vikram Persona)
```bash
./test_conversation.sh
```

**Expected Behavior:**
- Persona: Vikram (suspicious businessman)
- Responses: Mentions "CA", asks for verification
- Intel extraction: UPI ID, phone numbers

### Scenario 2: Single Message Test
```bash
./test_api.sh vikram     # GST scam
./test_api.sh priya      # Urgent bank scam
./test_api.sh suresh     # NRI scam
```

---

## Manual curl Testing

### Turn 1: Initial Scam Message
```bash
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -H "x-api-key: test-key" \
  -d '{
    "sessionId": "manual-test-001",
    "message": {
      "sender": "scammer",
      "text": "Your bank account will be blocked today. Verify immediately.",
      "timestamp": 1770005528731
    },
    "conversationHistory": [],
    "metadata": {
      "channel": "SMS",
      "language": "English",
      "locale": "IN"
    }
  }'
```

### Turn 2: Follow-up (with history)
```bash
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -H "x-api-key: test-key" \
  -d '{
    "sessionId": "manual-test-001",
    "message": {
      "sender": "scammer",
      "text": "Share your UPI ID to avoid suspension.",
      "timestamp": 1770005528732
    },
    "conversationHistory": [
      {
        "sender": "scammer",
        "text": "Your bank account will be blocked today. Verify immediately.",
        "timestamp": 1770005528731
      },
      {
        "sender": "user",
        "text": "ok which bank? send details",
        "timestamp": 1770005528731
      }
    ],
    "metadata": {
      "channel": "SMS",
      "language": "English",
      "locale": "IN"
    }
  }'
```

---

## Checking Results

### View Conversation Log
```bash
cat test_results_<session_id>.txt
```

### View Extracted Intelligence (JSON)
```bash
cat intelligence_reports/intel_<session_id>.json
```

Example output:
```json
{
  "sessionId": "test-session-123",
  "scamDetected": true,
  "totalMessagesExchanged": 7,
  "extractedIntelligence": {
    "bankAccounts": [],
    "upiIds": ["gst.payment@okaxis"],
    "phishingLinks": [],
    "phoneNumbers": ["9876543210", "+919876543210"],
    "suspiciousKeywords": ["urgent", "verify", "suspended"]
  },
  "agentNotes": "Scam confirmed after sufficient engagement. UPI IDs extracted: ['gst.payment@okaxis']; Phone numbers: ['9876543210', '+919876543210']"
}
```

---

## Configuration

### Environment Variables
- `LOCAL_FILE_MODE=true` - Write intelligence to files instead of POST
- `API_KEY=test-key` - API key for authentication
- `MISTRAL_API_KEY=<your-key>` - Mistral API key for LLM

### Callback Behavior

**Without LOCAL_FILE_MODE (Production):**
- Intelligence sent to `https://hackathon.guvi.in/api/updateHoneyPotFinalResult`
- Triggered after 3+ turns OR high-value intel detected
- One-time per session

**With LOCAL_FILE_MODE (Testing):**
- Intelligence written to `intelligence_reports/intel_<session_id>.json`
- Same trigger logic
- No network requests

---

## Troubleshooting

### Server not responding
```bash
# Check if server is running
curl http://localhost:8001/health

# Restart server
uv run uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### No intelligence extracted
- Check server logs for `[LOCAL FILE MODE]` or `[CALLBACK]` messages
- Verify scam is detected (needs 3+ turns OR high-value intel)
- Check `intelligence_reports/` directory

### Persona not working
- Verify persona selection logic in terminal output
- Expected personas: Vikram (business), Priya (urgent), Suresh (NRI), Rajesh (default)
