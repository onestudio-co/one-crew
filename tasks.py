from crewai import Task
import json

def create_tasks(agents, venture_idea, config_file="workshop_config.json"):
    """
    Create all the tasks for the workshop based on a JSON configuration file.

    Args:
        agents: Dictionary of agents with their IDs as keys
        venture_idea: Description of the venture idea
        config_file: Path to the JSON configuration file

    Returns:
        Dictionary of tasks with their IDs as keys
    """
    # Load the configuration file
    with open(config_file, "r") as f:
        config = json.load(f)

    # Get the negotiation instructions from the config
    negotiation_instructions = config.get("negotiation_instructions", "")

    # Create a dictionary to store tasks
    tasks = {}
    task_objects = {}

    # Create tasks based on the configuration
    for i, task_config in enumerate(config["tasks"]):
        # Replace placeholders in the description
        description = task_config["description"]
        description = description.replace("{venture_idea}", venture_idea)
        description = description.replace("{negotiation_instructions}", negotiation_instructions)

        # Replace task output references with actual task outputs
        for context_task_id in task_config.get("context", []):
            if context_task_id in task_objects:
                placeholder = f"{{{context_task_id}_task.output}}"
                description = description.replace(placeholder, f"{{{task_objects[context_task_id].output}}}")

        # Special handling for the first task - full team collaboration
        if i == 0:  # First task
            team_collaboration_instructions = """
            IMPORTANT: FULL TEAM COLLABORATION REQUIRED

            This is the first and most critical task of the workshop. ALL TEAM MEMBERS must actively participate.

            Before finalizing your answer:
            1. You MUST consult with EVERY other agent in the crew
            2. Each agent must provide their unique perspective based on their role and expertise
            3. Document each agent's contribution in your final output
            4. Synthesize all perspectives into a cohesive recommendation
            5. Only proceed when you have incorporated feedback from the entire team

            Your final output must include a detailed collaboration section listing input from each agent.

            The success of the entire workshop depends on getting this foundation right with full team input.
            """
            description = description + "\n\n" + team_collaboration_instructions
        else:  # All other tasks
            collaborative_instructions = """
            Important: This is a collaborative task. You should actively consult with other agents in the crew to get their perspectives and expertise. Consider the following:
            1. Ask other agents for their input on specific aspects of the task
            2. Request feedback on your initial ideas
            3. Incorporate diverse viewpoints into your final output
            4. Acknowledge contributions from other agents

            The final output should represent a synthesis of the collective intelligence of the crew.
            """
            description = description + "\n\n" + collaborative_instructions

        # Create the task
        task = Task(
            description=description,
            agent=agents[task_config["agent_id"]],
            expected_output=task_config["expected_output"],
            context=[task_objects[context_id] for context_id in task_config.get("context", []) if context_id in task_objects],
            allow_delegation=True  # Enable delegation to encourage collaboration
        )

        # Add the task to the dictionaries
        tasks[task_config["id"]] = task
        task_objects[task_config["id"]] = task

    # Return the list of tasks in the order specified in the config
    ordered_tasks = []
    for task_config in config["tasks"]:
        ordered_tasks.append(tasks[task_config["id"]])

    return ordered_tasks
