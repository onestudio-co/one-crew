# Workshop Configuration System

This document explains how to use the configuration-based system to create and run custom workshops.

## Overview

The workshop system has been redesigned to use a JSON configuration file that defines:

1. Workshop metadata (name, description)
2. Agent definitions (roles, goals, backstories)
3. Task definitions (descriptions, agent assignments, dependencies)

This allows you to create multiple workshop configurations for different purposes without changing the code.

## Configuration File Structure

The configuration file (`workshop_config.json`) has the following structure:

```json
{
  "workshop_name": "Workshop Name",
  "workshop_description": "Workshop description",
  "agents": [
    {
      "id": "agent_id",
      "role": "Agent Role",
      "goal": "Agent Goal",
      "backstory": "Agent Backstory",
      "verbose": true,
      "allow_delegation": true,
      "tools": ["tool_name1", "tool_name2"]
    },
    ...
  ],
  "tasks": [
    {
      "id": "task_id",
      "description": "Task description with placeholders: {venture_idea}, {negotiation_instructions}",
      "agent_id": "agent_id",
      "expected_output": "Expected output description",
      "context": ["dependency_task_id1", "dependency_task_id2"]
    },
    ...
  ],
  "negotiation_instructions": "Common instructions for all tasks"
}
```

## Creating a Custom Workshop

To create a custom workshop:

1. Copy the `workshop_config.json` file to a new file (e.g., `my_workshop_config.json`)
2. Modify the workshop name, description, agents, and tasks as needed
3. Run the workshop with your custom configuration:

```bash
python venture_workshop.py
# When prompted, enter the path to your custom configuration file
```

## Agent Configuration

Each agent requires:

- `id`: Unique identifier for the agent
- `role`: The agent's role/title
- `goal`: The agent's primary goal
- `backstory`: Detailed backstory that shapes the agent's personality and expertise
- `verbose`: Whether to show detailed output (usually true)
- `allow_delegation`: Whether the agent can delegate tasks (usually true)
- `tools`: List of tool names the agent can use (optional)

## Task Configuration

Each task requires:

- `id`: Unique identifier for the task
- `description`: Detailed task description with placeholders:
  - `{venture_idea}`: Will be replaced with the user's input
  - `{negotiation_instructions}`: Will be replaced with common instructions
  - `{task_id_task.output}`: Will be replaced with the output of a dependency task
- `agent_id`: ID of the agent assigned to this task
- `expected_output`: Description of what the task should produce
- `context`: List of task IDs that this task depends on (optional)

## Available Tools

The following tools are available for agents:

- `market_research_tool`: For market research and competitive analysis
- `financial_modeling_tool`: For financial projections and ROI calculations
- `technical_assessment_tool`: For technical feasibility and development cost estimation
- `validation_experiment_tool`: For designing validation experiments
- `pivot_analysis_tool`: For analyzing business model pivots

## Example: Creating a Simplified Workshop

Here's an example of creating a simplified workshop with fewer steps:

```json
{
  "workshop_name": "Quick Monetization Assessment",
  "workshop_description": "A streamlined assessment of monetization options",
  "agents": [
    {
      "id": "strategist",
      "role": "Business Strategist",
      "goal": "Identify the most promising monetization options",
      "backstory": "You are an experienced business strategist...",
      "verbose": true,
      "allow_delegation": true,
      "tools": []
    },
    {
      "id": "analyst",
      "role": "Financial Analyst",
      "goal": "Assess financial viability of monetization options",
      "backstory": "You are a financial analyst with expertise...",
      "verbose": true,
      "allow_delegation": true,
      "tools": ["financial_modeling_tool"]
    }
  ],
  "tasks": [
    {
      "id": "venture_assessment",
      "description": "Assess the venture idea and identify potential monetization options.\n\nVenture Idea: {venture_idea}\n\n{negotiation_instructions}",
      "agent_id": "strategist",
      "expected_output": "Assessment of the venture and potential monetization options",
      "context": []
    },
    {
      "id": "financial_analysis",
      "description": "Analyze the financial viability of the monetization options.\n\nVenture Assessment: {venture_assessment_task.output}\n\n{negotiation_instructions}",
      "agent_id": "analyst",
      "expected_output": "Financial analysis of monetization options",
      "context": ["venture_assessment"]
    }
  ],
  "negotiation_instructions": "Important Instructions:\n1. Use web search to gather up-to-date market data\n2. Be concise and actionable in your recommendations"
}
```

## Best Practices

1. **Task Dependencies**: Make sure task dependencies are correctly specified in the `context` array
2. **Agent Specialization**: Create agents with clear, specialized roles
3. **Task Clarity**: Provide detailed instructions in task descriptions
4. **Negotiation Instructions**: Use the common negotiation instructions for guidance that applies to all tasks
5. **Testing**: Test your configuration with simple inputs before running a full workshop
