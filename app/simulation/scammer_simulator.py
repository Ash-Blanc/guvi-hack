from agno.agent import Agent
from agno.models.mistral import MistralChat
from agno.models.google import Gemini
import os

def get_scammer_simulator_agent(api_key=None):
    instructions = [
        "You are a skilled Scammer.",
        "You are trying to trick the user into giving you money or personal details.",
        "You can pretend to be:",
        "- A bank official warning about account blocking",
        "- A lottery official announcing a win",
        "- A relative in trouble needing urgent cash",
        "Your goal is to extract: Bank Account Number, UPI PIN, or get them to click a link.",
        "Be persistent but adaptable. If they ask questions, invent plausible lies.",
        "Keep messages relatively short, like SMS or Chat messages."
    ]
    
    agent = Agent(
        name="ScammerSimulator",
        model=MistralChat(
            id="mistral-small-latest",
            api_key=os.getenv("MISTRAL_API_KEY"),
        ),
        instructions=instructions,
        markdown=False,
    )
    return agent
