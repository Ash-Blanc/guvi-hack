import os
import langwatch
from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.openai.like import OpenAILike
from agno.models.mistral import MistralChat
from openinference.instrumentation.agno import AgnoInstrumentor
from .intelligence import extract_intelligence, is_scam
from .models import APIResponse, APIRequest, Message

# Setup LangWatch instrumentation
langwatch.setup(instrumentors=[AgnoInstrumentor()])

import yaml

def get_honeypot_agent(db=None):
    # Load prompt from YAML as a fallback for sync issues
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "honeypot_agent.prompt.yaml")
    instructions = []
    try:
        with open(prompt_path, 'r') as f:
            prompt_config = yaml.safe_load(f)
            for msg in prompt_config.get('messages', []):
                if msg.get('role') == 'system':
                    instructions.append(msg.get('content'))
    except Exception as e:
        print(f"Warning: Could not load prompt from {prompt_path}: {e}")
        instructions = [
            "1. Analyze the incoming message for scam intent.",
            "2. If it's a scam, respond in character to engage them and delay them.",
            "3. Extract any bank info, UPI IDs or links they share.",
            "4. Never admit you are an AI or that you know it's a scam.",
        ]
    
    agent = Agent(
        name="HoneypotAgent",
        # model=Gemini(id="gemini-1.5-flash"),
        # model=OpenAILike(
        #     id="openai",
        #     base_url="https://text.pollinations.ai/nova-fast",
        #     api_key=os.getenv("POLLINATIONS_API_KEY", "pollinations"),
        # ),
        model=MistralChat(
            id="mistral-large-latest",
            api_key=os.getenv("MISTRAL_API_KEY"),
        ),
        description="You are a human-like honeypot agent engaging scammers. You can extract intelligence tools to analyze messages.",
        instructions=instructions + ["Use the `extract_intelligence` tool to scan incoming messages for bank details, UPIs, or phone numbers if they look suspicious."],
        tools=[extract_intelligence],
        markdown=False,
        db=db,
    )

    return agent


async def process_message(request: APIRequest) -> APIResponse:
    text = request.message.text
    history = "\n".join([f"{m.sender}: {m.text}" for m in request.conversationHistory])
    
    # Extract intelligence locally first
    extracted = extract_intelligence(text)
    scam_detected = is_scam(text, extracted)
    
    # Get agent response
    agent = get_honeypot_agent()
    
    # Prepare the query for the agent incorporating context
    query = f"Incoming Message: {text}\nHistory: {history}\nMetadata: {request.metadata}"
    
    # In a real scenario, we'd use Structured Output
    # For this hackathon, we want a fast respond back
    response = agent.run(query)
    
    # The agent prompt instructed it to return JSON or a human message
    # We ensure we return the required APIResponse format
    reply = response.content if response.content else "I'm not sure I understand. Can you explain more?"
    
    return APIResponse(status="success", reply=reply)
