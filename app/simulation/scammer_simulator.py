from agno.agent import Agent
from agno.models.mistral import MistralChat
from agno.models.google import Gemini
from ..config import SIMULATOR_MODEL_ID
import os

def get_scammer_simulator_agent(api_key=None):
    instructions = [
        "You are a scammer trying to trick the user into revealing their bank details or sending money.",
        "Use urgent language and threats of account blockage.",
        "Try to get OTPs, UPI PINs, or card details.",
        "If the user asks questions, make up plausible but fake answers.",
        "Do not reveal that you are an AI."
    ]
    
    agent = Agent(
        name="ScammerSimulator",
        model=MistralChat(
            id=SIMULATOR_MODEL_ID,
            api_key=os.getenv("MISTRAL_API_KEY"),
        ),
        instructions=instructions,
        markdown=False,
    )
    return agent
