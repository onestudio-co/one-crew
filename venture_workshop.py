from crewai import Crew, Process, Task
from langchain_openai import ChatOpenAI
import os
import datetime
import psutil
import json
import time
import tiktoken
from pathlib import Path
from dotenv import load_dotenv
from agents import create_agents
from tasks import create_tasks
from config import OPENAI_MODEL, AGENT_TEMPERATURE
from utils import format_workshop_output

# Cost tracking constants
MODEL_COSTS = {
    "gpt-4-1106-preview": {"input": 0.01, "output": 0.03},  # $0.01 per 1K input tokens, $0.03 per 1K output tokens
    "gpt-4-0125-preview": {"input": 0.01, "output": 0.03},  # $0.01 per 1K input tokens, $0.03 per 1K output tokens
    "gpt-4-turbo-preview": {"input": 0.01, "output": 0.03},  # $0.01 per 1K input tokens, $0.03 per 1K output tokens
    "gpt-4": {"input": 0.03, "output": 0.06},  # $0.03 per 1K input tokens, $0.06 per 1K output tokens
    "gpt-4-32k": {"input": 0.06, "output": 0.12},  # $0.06 per 1K input tokens, $0.12 per 1K output tokens
    "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002}  # $0.0015 per 1K input tokens, $0.002 per 1K output tokens
}

# Function to count tokens
def count_tokens(text, model="gpt-4"):
    """Count the number of tokens in a text string."""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception as e:
        print(f"Error counting tokens: {e}")
        # Fallback: estimate tokens as words / 0.75 (rough approximation)
        return int(len(text.split()) / 0.75)

# Function to calculate cost
def calculate_cost(input_tokens, output_tokens, model=OPENAI_MODEL):
    """Calculate the cost of API usage based on tokens and model."""
    # Default to gpt-4 costs if model not found
    costs = MODEL_COSTS.get(model, MODEL_COSTS["gpt-4"])
    input_cost = (input_tokens / 1000) * costs["input"]
    output_cost = (output_tokens / 1000) * costs["output"]
    return input_cost + output_cost

# Load environment variables
load_dotenv()

# Initialize the OpenAI API with your key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Initialize the LLM with web browsing capabilities
llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=AGENT_TEMPERATURE,
    api_key=openai_api_key,
    tools=[{"type": "web_search"}]  # Enable web search capability
)

def run_venture_workshop(venture_idea, config_file="workshop_config.json"):
    """
    Run the venture monetization workshop for a given idea.

    Args:
        venture_idea: A brief description of the venture idea
        config_file: Path to the JSON configuration file

    Returns:
        The complete workshop output
    """
    # Create reports directory if it doesn't exist
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    # Create a timestamp for this workshop
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"Running monetization workshop for venture: {venture_idea}")
    print(f"Using model: {OPENAI_MODEL}")
    print(f"Using configuration from: {config_file}")

    # Create agents
    print("Creating agents from configuration...")
    agent_dict = create_agents(llm, config_file)

    # Create tasks
    print("Setting up workshop tasks from configuration...")
    tasks = create_tasks(agent_dict, venture_idea, config_file)

    # Create the crew
    print("Assembling the crew...")
    crew = Crew(
        agents=list(agent_dict.values()),  # Convert dictionary to list for CrewAI
        tasks=tasks,
        verbose=True,
        process=Process.hierarchical,  # Use hierarchical process to enable collaboration
        manager_llm=llm  # Use the same LLM for the manager agent
    )

    # Create a function to update the progress report
    def update_progress_report(completed_tasks, task_costs=None):
        # Create a progress report
        progress_report = f"# GCC/MENA Venture Monetization Workshop - Progress Report\n\n"
        progress_report += f"## Venture Idea\n\n{venture_idea}\n\n"
        progress_report += f"## Progress: {len(completed_tasks)} of {len(tasks)} steps completed\n\n"

        # Add cost summary if available
        if task_costs:
            total_cost = sum(cost_data["cost"] for cost_data in task_costs.values())
            total_input_tokens = sum(cost_data["input_tokens"] for cost_data in task_costs.values())
            total_output_tokens = sum(cost_data["output_tokens"] for cost_data in task_costs.values())
            total_execution_time = sum(cost_data["execution_time"] for cost_data in task_costs.values())

            progress_report += f"## Cost Summary\n\n"
            progress_report += f"- **Total Cost**: ${total_cost:.4f}\n"
            progress_report += f"- **Total Tokens**: {total_input_tokens:,} input, {total_output_tokens:,} output\n"
            progress_report += f"- **Total Execution Time**: {total_execution_time:.2f} seconds\n\n"

        # Add completed steps
        progress_report += f"## Completed Steps\n\n"
        for i, (task_name, task_output) in enumerate(completed_tasks.items(), 1):
            # Extract the outcome section if available
            # Make sure task_output is a string
            task_output_str = str(task_output)
            outcome = task_output_str
            if "# Outcome" in task_output_str:
                outcome = task_output_str.split("# Outcome")[1].split("# Collaboration Summary")[0].strip()

            progress_report += f"### Step {i}: {task_name}\n\n"
            progress_report += f"#### Outcome\n{outcome}\n\n"

            # Add cost information if available
            if task_costs and task_name in task_costs:
                cost_data = task_costs[task_name]
                progress_report += f"#### Task Metrics\n"
                progress_report += f"- **Cost**: ${cost_data['cost']:.4f}\n"
                progress_report += f"- **Tokens**: {cost_data['input_tokens']:,} input, {cost_data['output_tokens']:,} output\n"
                progress_report += f"- **Execution Time**: {cost_data['execution_time']:.2f} seconds\n\n"

            # Add a link to the detailed explanation
            progress_report += f"[View detailed explanation](#step-{i}-details)\n\n"

        # Add detailed explanations in a separate section
        progress_report += f"## Detailed Explanations\n\n"
        for i, (task_name, task_output) in enumerate(completed_tasks.items(), 1):
            progress_report += f"<a id='step-{i}-details'></a>\n"
            progress_report += f"### Step {i}: {task_name} - Details\n\n"
            progress_report += f"{task_output}\n\n"

        # Add footer
        progress_report += "\n---\n\n"
        progress_report += f"*Progress report generated at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        progress_report += f"*This workshop is being conducted using {OPENAI_MODEL} with web browsing capabilities.*\n"
        if task_costs:
            total_cost = sum(cost_data["cost"] for cost_data in task_costs.values())
            progress_report += f"*Estimated total cost: ${total_cost:.4f}*\n"

        # Save the progress report
        with open("venture_workshop_results.md", "w") as f:
            f.write(progress_report)

        # Also save a timestamped version in the reports directory
        report_path = reports_dir / f"workshop_progress_{timestamp}_step{len(completed_tasks)}.md"
        with open(report_path, "w") as f:
            f.write(progress_report)

        print(f"\nProgress report updated: {len(completed_tasks)} of {len(tasks)} steps completed.")
        print(f"Report saved to venture_workshop_results.md and {report_path}\n")

    # Run the crew with step-by-step reporting
    print("\nStarting the GCC/MENA Venture Monetization Workshop...\n")
    print("This process will take some time as our agents work through each step.")
    print("Please be patient while the workshop is in progress.\n")

    # Initialize empty dictionaries to store completed tasks and costs
    completed_tasks = {}
    task_costs = {}
    total_cost = 0
    total_tokens = {"input": 0, "output": 0}

    # Execute each task sequentially and update the report after each one
    for i, task in enumerate(tasks):
        task_name = task.description.split('\n')[0].strip()
        print(f"\nExecuting task {i+1} of {len(tasks)}: {task_name}")

        # Track start time
        start_time = time.time()

        # Estimate input tokens from task description
        task_input_tokens = count_tokens(task.description, OPENAI_MODEL)

        # Special handling for the first task - use all agents
        if i == 0:  # First task - full team collaboration
            print("\nThis is the first task - engaging the entire team for collaboration...")
            # Create a crew with all agents for the first task
            full_team_crew = Crew(
                agents=list(agent_dict.values()),  # All agents
                tasks=[task],
                verbose=True,
                process=Process.hierarchical,  # Use hierarchical process for collaboration
                manager_llm=llm  # Use the same LLM for the manager agent
            )
            # Execute the task with the full team
            task_result = full_team_crew.kickoff()
        else:  # All other tasks - single agent with collaboration
            # Get collaborators from config
            collaborators = []
            with open(config_file, "r") as f:
                config = json.load(f)
                for task_config in config["tasks"]:
                    if task_config["id"] == task.description.split('\n')[0].strip().lower().replace(" ", "_"):
                        if "collaborators" in task_config:
                            collaborator_ids = task_config["collaborators"]
                            collaborators = [agent_dict[agent_id] for agent_id in collaborator_ids if agent_id in agent_dict]
                        break

            # If collaborators found, add them to the crew
            if collaborators:
                agents_for_task = [task.agent] + collaborators
                print(f"Task will be executed by {task.agent.role} with collaboration from {', '.join([a.role for a in collaborators])}")
            else:
                agents_for_task = [task.agent]
                print(f"Task will be executed by {task.agent.role} without specific collaborators")

            # Create a single-task crew to execute just this task
            task_crew = Crew(
                agents=agents_for_task,
                tasks=[task],
                verbose=True,
                process=Process.hierarchical,  # Still use hierarchical for collaboration
                manager_llm=llm  # Use the same LLM for the manager agent
            )
            # Execute the task
            task_result = task_crew.kickoff()

        # Calculate execution time
        execution_time = time.time() - start_time

        # Convert result to string and estimate output tokens
        if hasattr(task_result, 'raw'):
            task_output = task_result.raw
        else:
            task_output = str(task_result)

        task_output_tokens = count_tokens(task_output, OPENAI_MODEL)

        # Calculate cost
        task_cost = calculate_cost(task_input_tokens, task_output_tokens, OPENAI_MODEL)
        total_cost += task_cost
        total_tokens["input"] += task_input_tokens
        total_tokens["output"] += task_output_tokens

        # Store the task result and metrics
        completed_tasks[task_name] = task_output
        task_costs[task_name] = {
            "execution_time": execution_time,
            "input_tokens": task_input_tokens,
            "output_tokens": task_output_tokens,
            "cost": task_cost
        }

        # Print cost information
        print(f"\nTask completed in {execution_time:.2f} seconds")
        print(f"Estimated tokens: {task_input_tokens:,} input, {task_output_tokens:,} output")
        print(f"Estimated cost: ${task_cost:.4f}")
        print(f"Total cost so far: ${total_cost:.4f}")

        # Update the progress report
        update_progress_report(completed_tasks, task_costs)

    # Format the final results
    # All values in completed_tasks should now be strings
    formatted_result = format_workshop_output("\n\n".join(completed_tasks.values()))

    # Save the final report
    with open("venture_workshop_results.md", "w") as f:
        f.write(formatted_result)

    # Also save a final version in the reports directory
    final_report_path = reports_dir / f"workshop_final_{timestamp}.md"
    with open(final_report_path, "w") as f:
        f.write(formatted_result)

    print(f"\nFinal workshop report saved to venture_workshop_results.md and {final_report_path}")

    return formatted_result

if __name__ == "__main__":
    # Check if a workshop is already in progress by looking for running processes
    current_pid = os.getpid()
    workshop_running = False

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Skip the current process
            if proc.info['pid'] == current_pid:
                continue

            # Check if it's a Python process running venture_workshop.py
            if proc.info['name'] == 'python' and any('venture_workshop.py' in cmd for cmd in proc.info['cmdline'] if cmd):
                workshop_running = True
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if workshop_running:
        print("A workshop is already running in another process.")
        print("You can view the progress in the venture_workshop_results.md file.")
        print("\nOptions:")
        print("1. Wait for the current workshop to complete")
        print("2. Kill the running workshop and start a new one")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ")

        if choice == '1':
            print("\nPlease check venture_workshop_results.md for progress updates.")
            exit(0)
        elif choice == '2':
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['pid'] != current_pid and proc.info['name'] == 'python' and \
                       any('venture_workshop.py' in cmd for cmd in proc.info['cmdline'] if cmd):
                        print(f"Terminating process {proc.info['pid']}...")
                        proc.terminate()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            print("Waiting for processes to terminate...")
            import time
            time.sleep(2)  # Give processes time to terminate
        else:
            print("Exiting.")
            exit(0)

    # Print welcome message
    print("=" * 80)
    print("Welcome to the GCC/MENA Venture Monetization Workshop!")
    print("=" * 80)
    print("\nThis workshop will help you identify and validate monetization streams")
    print("for your early-stage venture in the GCC/MENA region.")
    print("\nThe workshop follows a six-step process with stage-gating to ensure")
    print("all proposed monetization streams meet regional constraints and")
    print("early-stage funding limitations ($50K validation, $5K/month OPEX).")
    print("\nPlease provide a brief description of your venture idea:")

    # Get venture idea from user
    venture_idea = input("\nVenture Idea: ")

    # Ask for configuration file (optional)
    config_file = input("\nConfiguration file (press Enter for default workshop_config.json): ")
    if not config_file.strip():
        config_file = "workshop_config.json"

    # Verify the configuration file exists
    if not os.path.exists(config_file):
        print(f"\nError: Configuration file '{config_file}' not found.")
        print("Please make sure the file exists and try again.")
        exit(1)

    # Load the configuration to display workshop name
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
            workshop_name = config.get("workshop_name", "Venture Monetization Workshop")
            print(f"\nRunning workshop: {workshop_name}")
    except json.JSONDecodeError:
        print(f"\nError: Configuration file '{config_file}' is not valid JSON.")
        print("Please check the file format and try again.")
        exit(1)

    try:
        # Run the workshop
        result = run_venture_workshop(venture_idea, config_file)

        # Print the result
        print("\n\n" + "=" * 80)
        print("WORKSHOP RESULTS")
        print("=" * 80 + "\n")
        print(result)

        print(f"\nResults have been saved to venture_workshop_results.md")
        print(f"\nThank you for using the {workshop_name}!")
    except Exception as e:
        print(f"\nAn error occurred during the workshop: {e}")
        print("Please check the log files for more details.")
        import traceback
        traceback.print_exc()
