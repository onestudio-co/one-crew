from crewai import Agent
import json
from tools import (
    market_research_tool,
    financial_modeling_tool,
    technical_assessment_tool,
    validation_experiment_tool,
    pivot_analysis_tool
)
from config import AGENT_TEMPERATURE

# Map tool names to actual tool objects
TOOL_MAP = {
    "market_research_tool": market_research_tool,
    "financial_modeling_tool": financial_modeling_tool,
    "technical_assessment_tool": technical_assessment_tool,
    "validation_experiment_tool": validation_experiment_tool,
    "pivot_analysis_tool": pivot_analysis_tool
}

def create_agents(llm, config_file="workshop_config.json"):
    """
    Create all the agents for the workshop based on a JSON configuration file.

    Args:
        llm: The language model to use
        config_file: Path to the JSON configuration file

    Returns:
        Dictionary of agents with their IDs as keys
    """
    # Load the configuration file
    with open(config_file, "r") as f:
        config = json.load(f)

    # Create agents based on the configuration
    agents = {}
    for agent_config in config["agents"]:
        # Get the tools for this agent
        tools = []
        for tool_name in agent_config.get("tools", []):
            if tool_name in TOOL_MAP:
                tools.append(TOOL_MAP[tool_name])

        # Create the agent
        agent = Agent(
            role=agent_config["role"],
            goal=agent_config["goal"],
            backstory=agent_config["backstory"],
            verbose=agent_config.get("verbose", True),
            allow_delegation=agent_config.get("allow_delegation", True),
            tools=tools if tools else None,
            llm=llm
        )

        # Add the agent to the dictionary
        agents[agent_config["id"]] = agent

    return agents
