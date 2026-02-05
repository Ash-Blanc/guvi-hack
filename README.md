# Agentic Honey-Pot for Scam Detection & Intelligence Extraction

AI-powered honeypot system designed to detect scam messages, autonomously engage scammers in multi-turn conversations, extract actionable intelligence, and report findings.

## Features

- **Scam Detection**: Real-time analysis of incoming messages for fraudulent intent.
- **Autonomous Engagement**: Multi-turn conversational agent using Agno + Gemini 2.0 Flash.
- **Intelligence Extraction**: Automated extraction of bank accounts, UPI IDs, phone numbers, and phishing links.
- **GUVI Callback**: Automatic reporting of extracted intelligence to the evaluation endpoint.
- **Prompt Management**: Versioned prompts managed via LangWatch CLI.
- **Scenario Testing**: Comprehensive agent simulation tests with LangWatch Scenario.

## Setup

1. **Install Dependencies**:
   ```bash
   uv sync
   ```

2. **Configure Environment**:
   Copy `.env.example` to `.env` and add your API keys:
   - `GOOGLE_API_KEY`: For Gemini models.
   - `LANGWATCH_API_KEY`: For tracing and prompt management.
   - `API_KEY`: Set your desired API key for the honeypot endpoints (default: `test-key`).

3. **Sync Prompts**:
   ```bash
   langwatch prompt sync
   ```

## API Usage

### Analyze Message
Accepts scam messages and returns agent responses.

**Endpoint**: `POST /analyze`
**Headers**: `x-api-key: your-api-key`

**Request Body**:
```json
{
  "sessionId": "session-123",
  "message": {
    "sender": "scammer",
    "text": "Your bank account will be blocked today. Verify immediately at http://fake-bank.com",
    "timestamp": 1770005528731
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}
```

## Testing

Run the Scenario tests using pytest:
```bash
uv run pytest tests/scenarios/ -v
```

## Development

Run the FastAPI server locally:
```bash
uv run uvicorn app.main:app --reload
```
