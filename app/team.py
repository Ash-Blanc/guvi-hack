from agno.team import Team
from .agents.scam_detector import get_scam_detector_agent
from .agents.honeypot import get_honeypot_agent
from .personas import select_persona, format_persona_instructions


def get_fraud_detection_team(
    model_id: str = "mistral-small-latest",
    first_message: str = None,
    **kwargs
):
    """
    Create a fraud detection team with dynamic persona selection.
    
    The team leader (ScamDetector) analyzes messages and delegates
    to the HoneypotAgent when scams are detected. The HoneypotAgent
    uses a persona selected based on the scam type.
    """
    # Select persona based on first message if available
    if first_message:
        persona = select_persona(first_message)
        persona_context = f"The honeypot is playing '{persona.name}', a {persona.age}-year-old {persona.occupation}."
    else:
        persona_context = "The honeypot will adopt an appropriate persona."
    
    # Initialize members with potential persona hint
    honeypot = get_honeypot_agent(model_id=model_id, first_message=first_message, **kwargs)
    
    # Initialize the ScamDetector for leader model
    scam_detector = get_scam_detector_agent(model_id=model_id, **kwargs)
    
    # Simplified Leader Instructions
    leader_instructions = [
        "You are the Leader of the Fraud Detection Team.",
        "Analyze incoming messages for scam indicators:",
        "- Urgency/threats (blocked accounts, KYC requests, suspension)",
        "- Requests for UPI, OTP, bank details, or money",
        "- Suspicious/shortened links",
        "IF the message shows scam intent → Delegate to 'HoneypotAgent'.",
        "IF the message is safe → Reply with a helpful message saying it appears safe.",
        "IMPORTANT: When delegating to 'HoneypotAgent', DO NOT output any text, reasoning, or 'I will delegate'. Just execute the handoff silently.",
        persona_context,
    ] 

    # Create the Team with respond_directly=True for route-like behavior
    team = Team(
        name="FraudDetectionTeam",
        members=[honeypot],
        model=scam_detector.model,
        instructions=leader_instructions,
        description="A team that detects scams and engages scammers via creative honeypot personas.",
        respond_directly=True,
        **kwargs
    )
    
    return team
