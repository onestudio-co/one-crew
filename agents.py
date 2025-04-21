from crewai import Agent
import json
from langchain.tools import BaseTool
from tools import (
    market_research_tool,
    financial_modeling_tool,
    technical_assessment_tool,
    validation_experiment_tool,
    pivot_analysis_tool
)
from config import AGENT_TEMPERATURE

# Convert LangChain tools to CrewAI compatible format
def convert_to_crewai_tool(lc_tool):
    return {
        "name": lc_tool.name,
        "description": lc_tool.description,
        "func": lc_tool._run
    }

# Map tool names to actual tool objects
TOOL_MAP = {
    "market_research_tool": convert_to_crewai_tool(market_research_tool),
    "financial_modeling_tool": convert_to_crewai_tool(financial_modeling_tool),
    "technical_assessment_tool": convert_to_crewai_tool(technical_assessment_tool),
    "validation_experiment_tool": convert_to_crewai_tool(validation_experiment_tool),
    "pivot_analysis_tool": convert_to_crewai_tool(pivot_analysis_tool)
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
        agent_kwargs = {
            "role": agent_config["role"],
            "goal": agent_config["goal"],
            "backstory": agent_config["backstory"],
            "verbose": agent_config.get("verbose", True),
            "allow_delegation": True,  # Always enable delegation for collaboration
            "llm": llm
        }

        # Only add tools if we have any
        if tools:
            agent_kwargs["tools"] = tools

        # Create the agent
        agent = Agent(**agent_kwargs)

        # Add the agent to the dictionary
        agents[agent_config["id"]] = agent

    return agents
