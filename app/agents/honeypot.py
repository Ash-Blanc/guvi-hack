from agno.agent import Agent
from agno.models.mistral import MistralChat
from ..intelligence import extract_intelligence
from ..personas import select_persona, format_persona_instructions, get_persona_by_id, Persona
from app.load_balancer import get_mistral_key


def get_honeypot_agent(
    model_id: str = "mistral-small-latest",
    persona_id: str = None,
    first_message: str = None,
    **kwargs
):
    """
    Create a honeypot agent with a dynamically selected persona.
    
    Args:
        model_id: The LLM model to use
        persona_id: Optional specific persona ID to use
        first_message: The first scam message (used for persona selection if no ID given)
        **kwargs: Additional arguments passed to Agent
    
    Returns:
        Agent configured with the selected persona's characteristics
    """
    # Select persona based on provided ID or first message content
    if persona_id:
        persona = get_persona_by_id(persona_id)
    elif first_message:
        persona = select_persona(first_message)
    else:
        # Default to Rajesh if no context provided
        from ..personas import RAJESH
        persona = RAJESH
    
    # Get formatted instructions for this persona
    instructions = format_persona_instructions(persona)
    
    agent = Agent(
        name="HoneypotAgent",
        model=MistralChat(
            id=model_id,
            api_key=get_mistral_key(),
        ),
        description=f"Honeypot agent playing '{persona.name}' - {persona.occupation}",
        instructions=instructions,
        tools=[extract_intelligence],
        markdown=False,
        **kwargs
    )
    return agent


def get_honeypot_agent_for_session(
    session_state: dict = None,
    first_message: str = None,
    model_id: str = "mistral-small-latest",
    **kwargs
):
    """
    Get or create a honeypot agent, maintaining persona consistency for a session.
    
    If session_state contains a persona_id, use that persona.
    Otherwise, select based on first_message and store in session_state.
    """
    persona_id = None
    
    # Check if session already has a persona assigned
    if session_state and "persona_id" in session_state:
        persona_id = session_state["persona_id"]
    elif first_message:
        # Select and store persona for new session
        persona = select_persona(first_message)
        persona_id = persona.id
        if session_state is not None:
            session_state["persona_id"] = persona_id
    
    return get_honeypot_agent(
        model_id=model_id,
        persona_id=persona_id,
        first_message=first_message,
        **kwargs
    )
