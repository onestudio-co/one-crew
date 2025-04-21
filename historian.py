# This file is kept for backward compatibility
# The historian agent is now defined in the workshop_config.json file
# and loaded by the create_agents function in agents.py

from config import OPENAI_MODEL, AGENT_TEMPERATURE

def create_historian_agent(llm):
    """
    Create a Workshop Historian agent responsible for documenting the entire workshop process.
    This function is kept for backward compatibility.

    Args:
        llm: The language model to use

    Returns:
        The Workshop Historian agent from the agents dictionary
    """
    from agents import create_agents

    # Create all agents from the config file
    agents = create_agents(llm)

    # Return the historian agent
    return agents["historian"]
