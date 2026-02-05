import json
from typing import Optional
from agno.agent import Agent
from agno.models.mistral import MistralChat
from agno.models.google import Gemini
from pydantic import BaseModel, Field
from app.load_balancer import get_mistral_key

class ScamDetectionResult(BaseModel):
    is_scam: bool = Field(..., description="Whether the message is detected as a scam.")
    confidence: float = Field(..., description="Confidence score between 0.0 and 1.0.")
    reasoning: str = Field(..., description="Brief explanation of why it is or isn't a scam.")
    scam_type: Optional[str] = Field(None, description="Type of scam (e.g., Phishing, UPI Fraud, OTP, Lottery) if detected.")

def get_scam_detector_agent(model_id: str = "mistral-large-latest", **kwargs):
    instructions = [
        "You are an expert Cyber Security Analyst specialized in detecting social engineering and financial scams.",
        "Analyze the incoming message for common scam indicators:",
        "- Urgency (e.g., 'immediately', 'blocked today')",
        "- Threats (e.g., 'police case', 'account suspended')",
        "- Unexpected financial requests (e.g., UPI, OTP info)",
        "- Suspicious links (shortened or mimicking banks)",
        "Determine if the message is a scam.",
        "Return your analysis as a valid JSON object with keys: is_scam (bool), confidence (float), reasoning (str), scam_type (str or null).",
        "Do not output markdown code blocks, just the raw JSON string."
    ]
    
    agent = Agent(
        name="ScamDetector",
        model=MistralChat(
            id=model_id,
            api_key=get_mistral_key(),
        ),
        description="Analyzes messages for scam intent.",
        instructions=instructions,
        markdown=False,
        **kwargs
    )
    return agent
