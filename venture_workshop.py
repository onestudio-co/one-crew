from crewai import Crew, Process, Task
from langchain_openai import ChatOpenAI
import os
import datetime
import psutil
import json
from pathlib import Path
from dotenv import load_dotenv
from agents import create_agents
from tasks import create_tasks
from config import OPENAI_MODEL, AGENT_TEMPERATURE
from utils import format_workshop_output

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
    def update_progress_report(completed_tasks):
        # Create a progress report
        progress_report = f"# GCC/MENA Venture Monetization Workshop - Progress Report\n\n"
        progress_report += f"## Venture Idea\n\n{venture_idea}\n\n"
        progress_report += f"## Progress: {len(completed_tasks)} of {len(tasks)} steps completed\n\n"

        # Add completed steps
        progress_report += f"## Completed Steps\n\n"
        for i, (task_name, task_output) in enumerate(completed_tasks.items(), 1):
            # Extract the outcome section if available
            # Make sure task_output is a string
            task_output_str = str(task_output)
            outcome = task_output_str
            if "# Outcome" in task_output_str:
                outcome = task_output_str.split("# Outcome")[1].split("# Explanation")[0].strip()

            progress_report += f"### Step {i}: {task_name}\n\n"
            progress_report += f"#### Outcome\n{outcome}\n\n"

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
        progress_report += "*This workshop is being conducted using CrewAI with GPT-4.1 and web browsing capabilities.*\n"

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

    # Initialize an empty dictionary to store completed tasks
    completed_tasks = {}

    # Execute each task sequentially and update the report after each one
    for i, task in enumerate(tasks):
        task_name = task.description.split('\n')[0].strip()
        print(f"\nExecuting task {i+1} of {len(tasks)}: {task_name}")

        # Create a single-task crew to execute just this task
        single_task_crew = Crew(
            agents=[task.agent],
            tasks=[task],
            verbose=True,
            process=Process.sequential
        )

        # Execute the task
        task_result = single_task_crew.kickoff()

        # Store the task result (convert CrewOutput to string)
        if hasattr(task_result, 'raw'):
            completed_tasks[task_name] = task_result.raw
        else:
            completed_tasks[task_name] = str(task_result)

        # Update the progress report
        update_progress_report(completed_tasks)

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
