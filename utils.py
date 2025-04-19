import re
import json

def format_markdown_table(headers, rows):
    """
    Format data as a markdown table.

    Args:
        headers: List of column headers
        rows: List of rows, where each row is a list of values

    Returns:
        Formatted markdown table as a string
    """
    # Ensure all rows have the same number of columns as headers
    for i, row in enumerate(rows):
        if len(row) < len(headers):
            rows[i] = row + [""] * (len(headers) - len(row))
        elif len(row) > len(headers):
            rows[i] = row[:len(headers)]

    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    # Create header row
    header_row = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"

    # Create separator row
    separator_row = "| " + " | ".join("-" * col_widths[i] for i in range(len(headers))) + " |"

    # Create data rows
    data_rows = []
    for row in rows:
        data_rows.append("| " + " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)) + " |")

    # Combine all rows
    table = "\n".join([header_row, separator_row] + data_rows)

    return table

def validate_constraints(data, constraint_type):
    """
    Validate that data meets the specified constraints.

    Args:
        data: Data to validate
        constraint_type: Type of constraint to check

    Returns:
        (bool, str): Tuple of (is_valid, error_message)
    """
    if constraint_type == "validation_budget":
        # Check if any stream exceeds $50K validation budget
        for stream in data.get("streams", []):
            if stream.get("one_time_cost", 0) > 50000:
                return False, f"Stream '{stream.get('name', 'Unknown')}' exceeds $50K validation budget constraint."
        return True, ""

    elif constraint_type == "monthly_opex":
        # Check if any stream exceeds $5K monthly OPEX
        for stream in data.get("streams", []):
            if stream.get("monthly_opex", 0) > 5000:
                return False, f"Stream '{stream.get('name', 'Unknown')}' exceeds $5K monthly OPEX constraint."
        return True, ""

    elif constraint_type == "stream_count":
        # Check if we have the required number of streams
        if len(data.get("streams", [])) < data.get("required_count", 0):
            return False, f"Not enough streams. Required: {data.get('required_count', 0)}, Found: {len(data.get('streams', []))}."
        return True, ""

    return True, ""

def extract_financial_metrics(text):
    """
    Extract financial metrics from text using regex.

    Args:
        text: Text containing financial metrics

    Returns:
        dict: Dictionary of extracted metrics
    """
    metrics = {}

    # Extract dollar amounts
    dollar_pattern = r'\$([0-9,]+(?:\.[0-9]{1,2})?)(K|M)?'
    dollar_matches = re.findall(dollar_pattern, text)

    for i, match in enumerate(dollar_matches):
        amount, unit = match
        amount = float(amount.replace(',', ''))
        if unit == 'K':
            amount *= 1000
        elif unit == 'M':
            amount *= 1000000

        metrics[f"dollar_amount_{i+1}"] = amount

    # Extract percentages
    percentage_pattern = r'([0-9]+(?:\.[0-9]{1,2})?)%'
    percentage_matches = re.findall(percentage_pattern, text)

    for i, match in enumerate(percentage_matches):
        metrics[f"percentage_{i+1}"] = float(match)

    # Extract time periods
    time_pattern = r'([0-9]+)[ -]*(day|week|month|year)s?'
    time_matches = re.findall(time_pattern, text)

    for i, match in enumerate(time_matches):
        amount, unit = match
        metrics[f"time_period_{i+1}"] = {
            "amount": int(amount),
            "unit": unit
        }

    return metrics

def format_workshop_output(results):
    """
    Format the final workshop output in a clean, structured format.

    Args:
        results: Raw workshop results (CrewOutput object or string)

    Returns:
        Formatted workshop output as a string
    """
    # Convert CrewOutput to string if needed
    if hasattr(results, 'raw'):
        # If it's a CrewOutput object, get the raw output
        results_text = results.raw
    else:
        # If it's already a string
        results_text = str(results)

    # Extract the Workshop Historian's documentation
    historian_documentation = None
    workshop_summary = None

    # Split the results by agent sections
    agent_sections = {}
    current_agent = None
    current_content = []

    lines = results_text.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('# Agent:'):
            # Save the previous agent's content
            if current_agent:
                agent_sections[current_agent] = '\n'.join(current_content)

            # Start a new agent section
            current_agent = line.replace('# Agent:', '').strip()
            current_content = []
        elif current_agent:
            current_content.append(line)

    # Save the last agent's content
    if current_agent:
        agent_sections[current_agent] = '\n'.join(current_content)

    # Extract the Workshop Historian's documentation
    if 'Workshop Historian' in agent_sections:
        historian_content = agent_sections['Workshop Historian']
        if '## Final Answer:' in historian_content:
            historian_documentation = historian_content.split('## Final Answer:')[1].strip()

    # Extract the Chief Strategy Officer's final summary
    if 'Chief Strategy Officer' in agent_sections:
        cso_content = agent_sections['Chief Strategy Officer']
        if '## Final Answer:' in cso_content:
            workshop_summary = cso_content.split('## Final Answer:')[1].strip()

    # Format the output
    formatted_output = "# GCC/MENA Venture Monetization Workshop Results\n\n"

    # Add the executive summary if available
    if workshop_summary:
        formatted_output += "## Executive Summary\n\n"
        formatted_output += workshop_summary + "\n\n"

    # Add the historian's documentation if available
    if historian_documentation:
        formatted_output += "## Detailed Workshop Documentation\n\n"
        formatted_output += historian_documentation + "\n\n"

    # If neither the summary nor documentation was found, fall back to the original approach
    if not workshop_summary and not historian_documentation:
        # Extract key sections
        sections = {}
        current_section = None

        for line in results_text.split('\n'):
            if line.startswith('# ') or line.startswith('## '):
                current_section = line.lstrip('#').strip()
                sections[current_section] = []
            elif current_section:
                sections[current_section].append(line)

        # Add venture description
        if "Venture Description" in sections:
            formatted_output += "## Venture Description\n\n"
            formatted_output += "\n".join(sections["Venture Description"]) + "\n\n"

        # Add prioritized streams
        if "Prioritized Streams" in sections:
            formatted_output += "## Top Monetization Streams\n\n"
            formatted_output += "\n".join(sections["Prioritized Streams"]) + "\n\n"

        # Add validation strategies
        if "Validation Strategy" in sections:
            formatted_output += "## Validation Strategies\n\n"
            formatted_output += "\n".join(sections["Validation Strategy"]) + "\n\n"

        # Add pivot implications
        if "Pivot Implications" in sections:
            formatted_output += "## Pivot Implications\n\n"
            formatted_output += "\n".join(sections["Pivot Implications"]) + "\n\n"

        # Add recommendations
        if "Recommendations" in sections:
            formatted_output += "## Recommendations\n\n"
            formatted_output += "\n".join(sections["Recommendations"]) + "\n\n"

        # If no sections were found, return the raw output
        if not sections:
            formatted_output += "## Raw Workshop Output\n\n"
            formatted_output += results_text

    # Add a footer with information about the workshop
    formatted_output += "\n---\n\n"
    formatted_output += "*This workshop was conducted using CrewAI with GPT-4.1 and web browsing capabilities. *\n"
    formatted_output += "*The complete workshop logs and detailed agent interactions are available in the logs directory.*\n"

    return formatted_output
