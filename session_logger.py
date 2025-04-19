import json
import logging
from datetime import datetime
from pathlib import Path

from crewai.utilities.events import (
    CrewKickoffStartedEvent,
    CrewKickoffCompletedEvent,
    AgentExecutionStartedEvent,
    AgentExecutionCompletedEvent,
    TaskStartedEvent,
    TaskCompletedEvent,
    LLMCallStartedEvent,
    LLMCallCompletedEvent,
    ToolUsageStartedEvent,
    ToolUsageFinishedEvent
)
from crewai.utilities.events.base_event_listener import BaseEventListener

class SessionLogger(BaseEventListener):
    """
    Custom event listener for logging CrewAI session events to a file.
    """
    def __init__(self, log_dir="logs"):
        super().__init__()
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        # Create a timestamp for this session
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"session_{self.timestamp}.log"
        self.json_log_file = self.log_dir / f"session_{self.timestamp}.json"

        # Initialize session data
        self.session_data = {
            "session_id": self.timestamp,
            "start_time": str(datetime.now()),
            "events": []
        }

        # Set up logging
        self.logger = logging.getLogger("CrewAI-Session")
        self.logger.setLevel(logging.INFO)

        # Create file handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.INFO)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.logger.info(f"Session logger initialized. Logs will be saved to {self.log_file} and {self.json_log_file}")

    def setup_listeners(self, crewai_event_bus):
        """
        Set up event listeners for the CrewAI event bus.
        """
        @crewai_event_bus.on(CrewKickoffStartedEvent)
        def on_crew_started(source, event):
            """Handle crew kickoff started event"""
            try:
                crew_name = getattr(event, 'crew_name', 'Unknown')
                self.logger.info(f"Crew '{crew_name}' started execution")

                # Add event to session data
                self.session_data["events"].append({
                    "event_type": "crew_started",
                    "timestamp": str(datetime.now()),
                    "crew_name": crew_name
                })

                # Save session data
                self._save_session_data()
            except Exception as e:
                self.logger.error(f"Error handling CrewKickoffStartedEvent: {e}")

        @crewai_event_bus.on(CrewKickoffCompletedEvent)
        def on_crew_completed(source, event):
            """Handle crew kickoff completed event"""
            try:
                crew_name = getattr(event, 'crew_name', 'Unknown')
                output = getattr(event, 'output', None)
                if hasattr(output, 'raw'):
                    output_str = output.raw
                else:
                    output_str = str(output) if output else "No output"

                self.logger.info(f"Crew '{crew_name}' completed execution")

                # Add event to session data
                self.session_data["events"].append({
                    "event_type": "crew_completed",
                    "timestamp": str(datetime.now()),
                    "crew_name": crew_name,
                    "output": output_str
                })

                # Add end time to session data
                self.session_data["end_time"] = str(datetime.now())

                # Save session data
                self._save_session_data()
            except Exception as e:
                self.logger.error(f"Error handling CrewKickoffCompletedEvent: {e}")

        @crewai_event_bus.on(AgentExecutionStartedEvent)
        def on_agent_execution_started(source, event):
            """Handle agent execution started event"""
            try:
                agent_role = "Unknown"
                if hasattr(event, 'agent') and event.agent:
                    if hasattr(event.agent, 'role'):
                        agent_role = event.agent.role

                task_description = ""
                if hasattr(event, 'task') and event.task:
                    if hasattr(event.task, 'description'):
                        task_description = event.task.description

                self.logger.info(f"Agent '{agent_role}' started task execution")

                # Add event to session data
                self.session_data["events"].append({
                    "event_type": "agent_execution_started",
                    "timestamp": str(datetime.now()),
                    "agent_role": agent_role,
                    "task_description": task_description
                })

                # Save session data
                self._save_session_data()
            except Exception as e:
                self.logger.error(f"Error handling AgentExecutionStartedEvent: {e}")

        @crewai_event_bus.on(AgentExecutionCompletedEvent)
        def on_agent_execution_completed(source, event):
            """Handle agent execution completed event"""
            try:
                agent_role = "Unknown"
                if hasattr(event, 'agent') and event.agent:
                    if hasattr(event.agent, 'role'):
                        agent_role = event.agent.role

                output = getattr(event, 'output', "No output")

                self.logger.info(f"Agent '{agent_role}' completed task execution")

                # Add event to session data
                self.session_data["events"].append({
                    "event_type": "agent_execution_completed",
                    "timestamp": str(datetime.now()),
                    "agent_role": agent_role,
                    "output": str(output)
                })

                # Save session data
                self._save_session_data()
            except Exception as e:
                self.logger.error(f"Error handling AgentExecutionCompletedEvent: {e}")

        @crewai_event_bus.on(TaskStartedEvent)
        def on_task_started(source, event):
            """Handle task started event"""
            try:
                task_description = getattr(event, 'task_description', 'Unknown task')

                self.logger.info(f"Task started: {task_description[:50]}...")

                # Add event to session data
                self.session_data["events"].append({
                    "event_type": "task_started",
                    "timestamp": str(datetime.now()),
                    "task_description": task_description
                })

                # Save session data
                self._save_session_data()
            except Exception as e:
                self.logger.error(f"Error handling TaskStartedEvent: {e}")

        @crewai_event_bus.on(TaskCompletedEvent)
        def on_task_completed(source, event):
            """Handle task completed event"""
            try:
                output = getattr(event, 'output', 'No output')

                self.logger.info(f"Task completed")

                # Add event to session data
                self.session_data["events"].append({
                    "event_type": "task_completed",
                    "timestamp": str(datetime.now()),
                    "output": str(output)
                })

                # Save session data
                self._save_session_data()
            except Exception as e:
                self.logger.error(f"Error handling TaskCompletedEvent: {e}")

        @crewai_event_bus.on(LLMCallStartedEvent)
        def on_llm_call_started(source, event):
            """Handle LLM call started event"""
            try:
                prompt = getattr(event, 'prompt', 'No prompt')

                self.logger.info(f"LLM call started")

                # Add event to session data
                self.session_data["events"].append({
                    "event_type": "llm_call_started",
                    "timestamp": str(datetime.now()),
                    "prompt": str(prompt)
                })

                # Save session data
                self._save_session_data()
            except Exception as e:
                self.logger.error(f"Error handling LLMCallStartedEvent: {e}")

        @crewai_event_bus.on(LLMCallCompletedEvent)
        def on_llm_call_completed(source, event):
            """Handle LLM call completed event"""
            try:
                response = getattr(event, 'response', 'No response')

                self.logger.info(f"LLM call completed")

                # Add event to session data
                self.session_data["events"].append({
                    "event_type": "llm_call_completed",
                    "timestamp": str(datetime.now()),
                    "response": str(response)
                })

                # Save session data
                self._save_session_data()
            except Exception as e:
                self.logger.error(f"Error handling LLMCallCompletedEvent: {e}")

        @crewai_event_bus.on(ToolUsageStartedEvent)
        def on_tool_usage_started(source, event):
            """Handle tool usage started event"""
            try:
                tool_name = getattr(event, 'tool_name', 'Unknown tool')
                tool_input = getattr(event, 'tool_input', 'No input')

                self.logger.info(f"Tool '{tool_name}' usage started")

                # Add event to session data
                self.session_data["events"].append({
                    "event_type": "tool_usage_started",
                    "timestamp": str(datetime.now()),
                    "tool_name": tool_name,
                    "tool_input": str(tool_input)
                })

                # Save session data
                self._save_session_data()
            except Exception as e:
                self.logger.error(f"Error handling ToolUsageStartedEvent: {e}")

        @crewai_event_bus.on(ToolUsageFinishedEvent)
        def on_tool_usage_finished(source, event):
            """Handle tool usage finished event"""
            try:
                tool_name = getattr(event, 'tool_name', 'Unknown tool')
                tool_output = getattr(event, 'tool_output', 'No output')

                self.logger.info(f"Tool '{tool_name}' usage finished")

                # Add event to session data
                self.session_data["events"].append({
                    "event_type": "tool_usage_finished",
                    "timestamp": str(datetime.now()),
                    "tool_name": tool_name,
                    "tool_output": str(tool_output)
                })

                # Save session data
                self._save_session_data()
            except Exception as e:
                self.logger.error(f"Error handling ToolUsageFinishedEvent: {e}")

    def _save_session_data(self):
        """Save session data to JSON file"""
        try:
            with open(self.json_log_file, 'w') as f:
                json.dump(self.session_data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving session data: {e}")

# Create an instance of the session logger
session_logger = SessionLogger()
