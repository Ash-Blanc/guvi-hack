import pytest
import scenario
from app.agent import get_honeypot_agent
from app.models import APIRequest, Message, Metadata
from app.intelligence import extract_intelligence, is_scam

# Configure Scenario to use a default model for simulations
# LangWatch recommended gpt-4o or similar for the user simulator
scenario.configure(default_model="gemini/gemini-2.0-flash")


class HoneypotScenarioAgent(scenario.AgentAdapter):
    async def call(self, input: scenario.AgentInput) -> scenario.AgentReturnTypes:
        # Create an APIRequest from the simulation input
        request = APIRequest(
            sessionId=input.thread_id,
            message=Message(
                sender="scammer",
                text=input.last_new_user_message_str(),
                timestamp=0
            ),
            conversationHistory=[
                Message(sender="scammer" if m.role == "user" else "assistant", text=str(m.content), timestamp=0)
                for m in input.messages[:-1]
            ],
            metadata=Metadata(channel="SMS", language="English", locale="IN")
        )
        
        # Get response from the actual agent logic
        agent = get_honeypot_agent()
        query = f"Incoming Message: {request.message.text}\nHistory: {[m.text for m in request.conversationHistory]}"
        response = agent.run(query)
        
        return str(response.content)

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_scam_engagement_and_intelligence():
    """
    Test that the agent detects a scam, maintains a persona, 
    and tries to extract intelligence without breaking character.
    """
    result = await scenario.run(
        name="bank fraud scam engagement",
        description="""
            A scammer sends a message about a blocked bank account.
            The user (honeypot) should act concerned and confused.
            Eventually, the scammer provides a fake UPI ID to 'verify' the account.
            The agent should extract this ID and continue the loop.
        """,
        agents=[
            HoneypotScenarioAgent(),
            scenario.UserSimulatorAgent(
                description="You are a scammer pretending to be a Bank Manager. You want to get the user to send money or reveal info."
            ),
            scenario.JudgeAgent(criteria=[
                "Agent maintains a human-like, concerned persona",
                "Agent does not reveal it is an AI or honeypot",
                "Agent successfully engages in a multi-turn conversation",
                "Agent's response is relevant to the scammer's message"
            ])
        ],
        script=[
            scenario.user("Urgent: Your HDFC account is blocked. Verify at http://bank-verify.in or pay 500 processing fee to upi@bank"),
            scenario.proceed()
        ],
        max_turns=5
    )
    
    assert result.success

@pytest.mark.unit
def test_intelligence_extraction_logic():
    """Unit test for the extraction regex logic."""
    text = "Send money to fraudster@upi and call +919876543210. Visit http://steal-data.com"
    extracted = extract_intelligence(text)
    
    assert "fraudster@upi" in extracted.upiIds
    assert "+919876543210" in extracted.phoneNumbers
    assert "http://steal-data.com" in extracted.phishingLinks
    assert is_scam(text, extracted) is True

