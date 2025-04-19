from crewai import Task

def create_tasks(agents, venture_idea):
    """
    Create all the tasks for the workshop.

    Args:
        agents: List of agents
        venture_idea: Description of the venture idea

    Returns:
        List of tasks
    """
    # Extract agents
    cso_agent = agents[0]
    cfo_agent = agents[1]
    cto_agent = agents[2]
    cpo_agent = agents[3]
    cmio_agent = agents[4]
    cxdo_agent = agents[5]
    coo_agent = agents[6]
    cdao_agent = agents[7]
    cpno_agent = agents[8]
    historian_agent = agents[9]  # Workshop Historian agent

    # Step 1: Define Venture Description
    venture_definition_task = Task(
        description=f"""Define a clear, concise value proposition and description for the venture idea:

        Venture Idea: {venture_idea}

        Your task is to:
        1. Craft a one-sentence value proposition that clearly articulates the unique value of this venture
        2. Write a one-paragraph description (no revenue details)

        Ensure the description is specific to the GCC/MENA market context and highlights the venture's unique value.

        Format your response with clear headings:
        # Venture Description
        ## Value Proposition
        [One-sentence value proposition]

        ## Description
        [One-paragraph description]
        """,
        agent=cso_agent,
        expected_output="A one-sentence value proposition and one-paragraph venture description"
    )

    # Step 2: Generate High-Level Streams
    high_level_streams_task = Task(
        description=f"""Generate 20 distinct, non-overlapping monetization options for the venture.

        Venture Description: {{venture_definition_task.output}}

        Your task is to:
        1. List 20 unique monetization streams that are suitable for a digital-first business in the GCC/MENA region
        2. Ensure each stream is distinct and non-overlapping with others
        3. For each stream, provide a name and a brief one-line description

        Format your response as a markdown table with columns for Stream Number, Stream Name, and Brief Description.

        # High-Level Monetization Streams
        [Table with 20 streams]
        """,
        agent=cmio_agent,
        expected_output="A table of 20 distinct monetization streams",
        context=[venture_definition_task]
    )

    # Step 3.1: Detail Realistic Streams - Stream Ideation
    stream_ideation_task = Task(
        description=f"""Select 10 of the most promising monetization streams that each require ≤ $50K total build cost.

        Monetization Streams: {{high_level_streams_task.output}}

        Your task is to:
        1. Review the 20 monetization streams
        2. Select the 10 most promising streams that can each be built and validated for ≤ $50K
        3. For each selected stream, provide:
           - Stream name
           - 1-2 sentence description
           - Initial thoughts on implementation approach

        Format your response as a markdown table with columns for Stream Number, Stream Name, Description, and Implementation Approach.

        # Selected Monetization Streams
        [Table with 10 selected streams]
        """,
        agent=cpo_agent,
        expected_output="A table of 10 selected monetization streams with descriptions",
        context=[venture_definition_task, high_level_streams_task]
    )

    # Step 3.2: Detail Realistic Streams - Revenue Estimation
    revenue_estimation_task = Task(
        description=f"""Estimate monthly revenue potential for each of the 10 selected streams using conservative GCC/MENA benchmarks.

        Selected Streams: {{stream_ideation_task.output}}

        Your task is to:
        1. For each of the 10 streams, estimate:
           - Monthly revenue potential (conservative estimate)
           - Key revenue drivers and assumptions
           - Ramp-up timeline (how long until the stream reaches this revenue)
        2. Include data sources and benchmarks used for your estimates
        3. Ensure all estimates are conservative and realistic for the GCC/MENA market

        Format your response as a markdown table with columns for Stream Number, Stream Name, Monthly Revenue Potential,
        Key Assumptions, Ramp-up Timeline, and Data Sources.

        # Revenue Estimates
        [Table with revenue estimates for 10 streams]
        """,
        agent=cfo_agent,
        expected_output="A table of revenue estimates for the 10 selected streams",
        context=[venture_definition_task, stream_ideation_task]
    )

    # Step 3.3: Detail Realistic Streams - Expense Estimation
    expense_estimation_task = Task(
        description=f"""Estimate one-time development cost and monthly OPEX for each of the 10 selected streams.

        Selected Streams: {{stream_ideation_task.output}}
        Revenue Estimates: {{revenue_estimation_task.output}}

        Your task is to:
        1. For each of the 10 streams, estimate:
           - One-time development/setup cost (must be ≤ $50K)
           - Monthly operational expenses (must be ≤ $5K/month)
           - Key cost components and assumptions
        2. Ensure all estimates are realistic for the GCC/MENA market
        3. Flag any streams that exceed the constraints

        Format your response as a markdown table with columns for Stream Number, Stream Name, One-time Cost,
        Monthly OPEX, Key Cost Components, and Notes/Assumptions.

        # Expense Estimates
        [Table with expense estimates for 10 streams]
        """,
        agent=cto_agent,
        expected_output="A table of expense estimates for the 10 selected streams",
        context=[venture_definition_task, stream_ideation_task, revenue_estimation_task]
    )

    # Step 4: Prioritize Top Streams
    prioritization_task = Task(
        description=f"""Select the 3 streams with the highest ROI and validation feasibility under $50K.

        Revenue Estimates: {{revenue_estimation_task.output}}
        Expense Estimates: {{expense_estimation_task.output}}

        Your task is to:
        1. Calculate ROI for each stream (consider both one-time costs and 12-month OPEX)
        2. Assess validation feasibility (how easily can the stream be tested with ≤ $50K)
        3. Select the top 3 streams based on ROI and validation feasibility
        4. Provide a 2-sentence rationale for each selected stream

        Format your response as a markdown table with columns for Priority, Stream Name, ROI (%),
        Validation Feasibility (High/Medium/Low), and Rationale.

        # Prioritized Streams
        [Table with top 3 prioritized streams]
        """,
        agent=cso_agent,
        expected_output="A table of the top 3 prioritized streams with rationale",
        context=[venture_definition_task, revenue_estimation_task, expense_estimation_task]
    )

    # Step 5: Validation Strategy
    validation_strategy_task = Task(
        description=f"""For each of the 3 prioritized streams, outline an MVP validation plan.

        Prioritized Streams: {{prioritization_task.output}}

        Your task is to:
        1. For each of the 3 streams, outline:
           - Validation steps (what needs to be built/tested)
           - Success criteria (what metrics indicate validation)
           - Timeline (how long the validation will take)
           - Estimated validation budget (must be ≤ $50K)
        2. Ensure the validation plan is lean, focused, and achievable

        Format your response as three separate sections (one for each stream) with bullet points for each component.

        # Validation Strategy
        ## Stream 1: [Name]
        [Validation plan details]

        ## Stream 2: [Name]
        [Validation plan details]

        ## Stream 3: [Name]
        [Validation plan details]
        """,
        agent=cpo_agent,
        expected_output="Validation plans for the top 3 streams",
        context=[venture_definition_task, prioritization_task]
    )

    # Step 6: Pivot Implications
    pivot_implications_task = Task(
        description=f"""For each of the 3 prioritized streams, state if it requires a business-model pivot.

        Venture Description: {{venture_definition_task.output}}
        Prioritized Streams: {{prioritization_task.output}}

        Your task is to:
        1. For each of the 3 streams, determine:
           - If it requires a business-model pivot (e.g., B2C→B2B, one-time vs. subscription)
           - What specific changes would be needed to the venture's core model
           - Draft an adjusted one-sentence venture description that incorporates the pivot
        2. Be specific about how the pivot affects the venture's target market, value proposition, and operations

        Format your response as three separate sections (one for each stream) with clear headings and bullet points.

        # Pivot Implications
        ## Stream 1: [Name]
        [Pivot details]

        ## Stream 2: [Name]
        [Pivot details]

        ## Stream 3: [Name]
        [Pivot details]
        """,
        agent=cpno_agent,
        expected_output="Pivot implications for the top 3 streams",
        context=[venture_definition_task, prioritization_task, validation_strategy_task]
    )

    # Final Workshop Summary
    workshop_summary_task = Task(
        description=f"""Create a comprehensive summary of the entire monetization workshop.

        Your task is to:
        1. Summarize the venture description
        2. List the top 3 prioritized monetization streams with their key metrics:
           - Estimated monthly revenue
           - One-time development cost
           - Monthly OPEX
           - ROI
           - Validation approach
           - Pivot implications
        3. Provide final recommendations for which stream to pursue first and why

        Format your response as a well-structured executive summary with clear sections and bullet points where appropriate.
        Ensure all information is presented in a concise, actionable format suitable for an early-stage venture in the GCC/MENA region.

        # Workshop Summary
        ## Venture Overview
        [Summary of venture]

        ## Top Monetization Streams
        [Summary of top 3 streams]

        ## Recommendations
        [Final recommendations]
        """,
        agent=cso_agent,
        expected_output="Comprehensive workshop summary with recommendations",
        context=[
            venture_definition_task,
            prioritization_task,
            validation_strategy_task,
            pivot_implications_task
        ]
    )

    # Historian Tasks - Document the workshop process
    step1_documentation_task = Task(
        description=f"""Document the venture definition process in detail.

        Your task is to:
        1. Observe and document the venture definition process
        2. Capture the key insights, reasoning, and decision-making process
        3. Document any discussions between agents
        4. Highlight the evolution of ideas and how the final definition was reached

        Format your response as a detailed report with sections for:
        - Process Overview
        - Key Discussions and Insights
        - Decision Points
        - Final Outcome

        # Step 1: Venture Definition Documentation
        [Detailed documentation]
        """,
        agent=historian_agent,
        expected_output="Detailed documentation of the venture definition process",
        context=[venture_definition_task]
    )

    step2_documentation_task = Task(
        description=f"""Document the monetization stream generation process in detail.

        Your task is to:
        1. Observe and document how the 20 monetization streams were generated
        2. Capture the market research, reasoning, and decision-making process
        3. Document any discussions between agents
        4. Highlight the key factors that influenced the selection of streams

        Format your response as a detailed report with sections for:
        - Process Overview
        - Market Research Insights
        - Decision Points
        - Final Outcome

        # Step 2: Monetization Stream Generation Documentation
        [Detailed documentation]
        """,
        agent=historian_agent,
        expected_output="Detailed documentation of the monetization stream generation process",
        context=[venture_definition_task, high_level_streams_task]
    )

    step3_documentation_task = Task(
        description=f"""Document the stream detailing and analysis process in detail.

        Your task is to:
        1. Observe and document how the streams were analyzed and detailed
        2. Capture the financial analysis, technical assessment, and decision-making process
        3. Document any discussions between agents
        4. Highlight the key factors that influenced the revenue and expense estimates

        Format your response as a detailed report with sections for:
        - Process Overview
        - Financial Analysis Insights
        - Technical Assessment Insights
        - Decision Points
        - Final Outcome

        # Step 3: Stream Detailing and Analysis Documentation
        [Detailed documentation]
        """,
        agent=historian_agent,
        expected_output="Detailed documentation of the stream detailing and analysis process",
        context=[stream_ideation_task, revenue_estimation_task, expense_estimation_task]
    )

    step4_5_6_documentation_task = Task(
        description=f"""Document the stream prioritization, validation, and pivot analysis process in detail.

        Your task is to:
        1. Observe and document how the streams were prioritized
        2. Capture the validation strategy development process
        3. Document the pivot implications analysis
        4. Highlight the key discussions, reasoning, and decision-making process

        Format your response as a detailed report with sections for:
        - Prioritization Process
        - Validation Strategy Development
        - Pivot Analysis
        - Key Discussions and Insights
        - Final Outcome

        # Steps 4-6: Prioritization, Validation, and Pivot Analysis Documentation
        [Detailed documentation]
        """,
        agent=historian_agent,
        expected_output="Detailed documentation of the prioritization, validation, and pivot analysis process",
        context=[prioritization_task, validation_strategy_task, pivot_implications_task]
    )

    workshop_documentation_task = Task(
        description=f"""Create a comprehensive documentation of the entire workshop process.

        Your task is to:
        1. Compile and synthesize the documentation from all workshop steps
        2. Create a cohesive narrative that shows the evolution of ideas throughout the workshop
        3. Highlight key discussions, insights, and decision points
        4. Document the reasoning behind each major decision
        5. Include relevant quotes or exchanges between agents that illustrate important points

        Format your response as a comprehensive report with clear sections for each workshop step,
        including an executive summary and a detailed appendix with supporting information.

        # Venture Monetization Workshop Documentation
        ## Executive Summary
        [Brief overview of the workshop process and outcomes]

        ## Workshop Process Documentation
        ### Step 1: Venture Definition
        [Detailed documentation]

        ### Step 2: Monetization Stream Generation
        [Detailed documentation]

        ### Step 3: Stream Detailing and Analysis
        [Detailed documentation]

        ### Steps 4-6: Prioritization, Validation, and Pivot Analysis
        [Detailed documentation]

        ## Key Insights and Learnings
        [Summary of the most important insights from the workshop]

        ## Appendix: Agent Discussions and Decision Points
        [Detailed documentation of significant discussions and decisions]
        """,
        agent=historian_agent,
        expected_output="Comprehensive documentation of the entire workshop process",
        context=[
            step1_documentation_task,
            step2_documentation_task,
            step3_documentation_task,
            step4_5_6_documentation_task,
            workshop_summary_task
        ]
    )

    # Create a list of all tasks
    main_tasks = [
        venture_definition_task,
        high_level_streams_task,
        stream_ideation_task,
        revenue_estimation_task,
        expense_estimation_task,
        prioritization_task,
        validation_strategy_task,
        pivot_implications_task,
        workshop_summary_task
    ]

    # Add historian tasks
    historian_tasks = [
        step1_documentation_task,
        step2_documentation_task,
        step3_documentation_task,
        step4_5_6_documentation_task,
        workshop_documentation_task
    ]

    # Return all tasks
    return main_tasks + historian_tasks
