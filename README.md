# CrewAI Venture Monetization Workshop

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A multi-agent AI system designed to run a rigorous, stage-gated monetization workshop for early-stage ventures in the GCC/MENA region. This project demonstrates the power of CrewAI for complex business strategy tasks.

## Overview

This application uses CrewAI to orchestrate a team of specialized AI agents that collaborate to analyze and develop monetization strategies for early-stage ventures. The workshop follows a structured six-step process with stage-gating to ensure that all proposed monetization streams meet the constraints of the GCC/MENA market and early-stage funding limitations.

## Features

- **Multi-Agent System**: Ten specialized agents including nine C-suite roles and a Workshop Historian
- **Stage-Gated Process**: Six-step workshop with validation at each stage
- **GCC/MENA Focus**: Conservative, realistic benchmarks for the Gulf Cooperation Council and Middle East/North Africa regions
- **Constraint Validation**: Ensures all streams meet funding constraints ($50K for validation, $5K/month OPEX)
- **Comprehensive Output**: Detailed analysis, prioritization, validation strategies, and pivot implications
- **Latest AI Model**: Uses OpenAI's GPT-4.1 model with web browsing capabilities for up-to-date information
- **Step-by-Step Reporting**: Generates progress reports after each step of the workshop
- **Detailed Documentation**: Workshop Historian agent documents the entire process, including discussions and decision-making

## Workshop Steps

1. **Define Venture Description**: Create a clear value proposition and description
2. **Generate High-Level Streams**: List 20 distinct monetization options
3. **Detail Realistic Streams**: Select and analyze 10 feasible streams
4. **Prioritize Top Streams**: Select the 3 streams with highest ROI and validation feasibility
5. **Validation Strategy**: Outline MVP validation plans for the top 3 streams
6. **Pivot Implications**: Analyze business model pivots required for each stream

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/onestudio-co/one-crew.git
   cd one-crew
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key in a `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Run the workshop with your venture idea:
   ```bash
   python venture_workshop.py
   ```

2. You will be prompted to enter a description of your venture idea.

3. The system will run the workshop step by step, updating the progress report after each step.

4. The final report will be saved to `venture_workshop_results.md` and also in the `reports` directory with a timestamp.

5. You can view the progress at any time by opening the `venture_workshop_results.md` file.

## Example

Here's an example of how to use the workshop:

```
$ python venture_workshop.py

Welcome to the GCC/MENA Venture Monetization Workshop!

This workshop will help you identify and validate monetization streams
for your early-stage venture in the GCC/MENA region.

Please provide a brief description of your venture idea:

Venture Idea: A mobile app that connects local artisans in the GCC region with customers looking for handmade, authentic products.
```

The system will then run the complete workshop and provide a detailed output with monetization strategies, validation plans, and recommendations.

## Agent Team

### C-Suite Agents

The workshop is run by a team of specialized C-suite agents:

- **Chief Strategy Officer (CSO)**: Sets vision, stage-gate criteria & kill rules
- **Chief Financial Officer (CFO)**: Builds conservative financial models, budgets & ROI analyses
- **Chief Technology Officer (CTO)**: Assesses technical feasibility, architecture & dev-cost estimates
- **Chief Product Officer (CPO)**: Defines feature prioritization, validation experiments & user-value hypotheses
- **Chief Market Intelligence Officer (CMIO)**: Conducts GCC-specific market studies & competitor scans
- **Chief UX & Design Officer (CXDO)**: Audits wireframes, prototypes & user flows for clarity and conversion
- **Chief Operations Officer (COO)**: Designs processes (legal, compliance, ops) and vendor-management
- **Chief Data & Analytics Officer (CDAO)**: Defines KPIs, dashboards & data-collection plans
- **Chief Partnerships & Negotiations Officer (CPNO)**: Sources & negotiates pilot deals, channel partnerships & B2B contracts

### Workshop Historian

In addition to the C-suite agents, the workshop includes a Workshop Historian agent:

- **Workshop Historian**: Documents the complete workshop process, including agent discussions, reasoning, and decisions. The historian creates a comprehensive report that shows the evolution of ideas throughout the workshop.

## Project Structure

```
venture-workshop/
├── agents.py             # Defines all agent roles and personalities
├── config.py             # Configuration settings
├── historian.py          # Workshop Historian agent definition
├── requirements.txt      # Project dependencies
├── tasks.py              # Workshop tasks and process flow
├── utils.py              # Utility functions
├── venture_workshop.py   # Main application entry point
└── reports/              # Generated reports directory
```

## Requirements

- Python 3.8+
- OpenAI API key with access to GPT-4.1
- Dependencies:
  - crewai
  - langchain
  - langchain_openai
  - python-dotenv
  - psutil

## Prompt Engineering

This project was developed with the assistance of AI (Claude and ChatGPT). For details on the prompt engineering techniques used to create this application, see the [PROMPT_ENGINEERING.md](PROMPT_ENGINEERING.md) file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
