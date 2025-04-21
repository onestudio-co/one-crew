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
    for task_config in config["tasks"]:
        # Replace placeholders in the description
        description = task_config["description"]
        description = description.replace("{venture_idea}", venture_idea)
        description = description.replace("{negotiation_instructions}", negotiation_instructions)

        # Replace task output references with actual task outputs
        for context_task_id in task_config.get("context", []):
            if context_task_id in task_objects:
                placeholder = f"{{{context_task_id}_task.output}}"
                description = description.replace(placeholder, f"{{{task_objects[context_task_id].output}}}")

        # Create the task
        task = Task(
            description=description,
            agent=agents[task_config["agent_id"]],
            expected_output=task_config["expected_output"],
            context=[task_objects[context_id] for context_id in task_config.get("context", []) if context_id in task_objects]
        )

        # Add the task to the dictionaries
        tasks[task_config["id"]] = task
        task_objects[task_config["id"]] = task

    # Return the list of tasks in the order specified in the config
    ordered_tasks = []
    for task_config in config["tasks"]:
        ordered_tasks.append(tasks[task_config["id"]])

    return ordered_tasks
