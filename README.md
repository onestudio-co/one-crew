# CrewAI Venture Monetization Workshop

A multi-agent AI system designed to run a rigorous, stage-gated monetization workshop for early-stage ventures in the GCC/MENA region.

## Overview

This application uses CrewAI to orchestrate a team of specialized AI agents that collaborate to analyze and develop monetization strategies for early-stage ventures. The workshop follows a structured six-step process with stage-gating to ensure that all proposed monetization streams meet the constraints of the GCC/MENA market and early-stage funding limitations.

## Features

- **Multi-Agent System**: Nine specialized C-suite agents with distinct roles and expertise
- **Stage-Gated Process**: Six-step workshop with validation at each stage
- **GCC/MENA Focus**: Conservative, realistic benchmarks for the Gulf Cooperation Council and Middle East/North Africa regions
- **Constraint Validation**: Ensures all streams meet funding constraints ($50K for validation, $5K/month OPEX)
- **Comprehensive Output**: Detailed analysis, prioritization, validation strategies, and pivot implications
- **Latest AI Model**: Uses OpenAI's GPT-4.1 model for advanced reasoning and analysis

## Workshop Steps

1. **Define Venture Description**: Create a clear value proposition and description
2. **Generate High-Level Streams**: List 20 distinct monetization options
3. **Detail Realistic Streams**: Select and analyze 10 feasible streams
4. **Prioritize Top Streams**: Select the 3 streams with highest ROI and validation feasibility
5. **Validation Strategy**: Outline MVP validation plans for the top 3 streams
6. **Pivot Implications**: Analyze business model pivots required for each stream

## Installation

1. Make sure you have Python 3.8+ installed
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key in a `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the workshop with your venture idea:

```
python venture_workshop.py
```

You will be prompted to enter a description of your venture idea. The system will then run the complete workshop and provide detailed output.

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

## C-Suite Agent Team

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

## Requirements

- Python 3.8+
- OpenAI API key
- CrewAI
- LangChain
- Other dependencies listed in requirements.txt

## License

MIT
