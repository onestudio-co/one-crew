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

    # Common task instructions to encourage negotiation and web research
    negotiation_instructions = """
    Important Instructions:
    1. Use web search to gather up-to-date market data, benchmarks, and industry trends for the GCC/MENA region
    2. Actively negotiate and discuss with other agents when you need additional input
    3. Challenge assumptions and provide evidence for your conclusions
    4. Consider regional constraints and cultural factors specific to GCC/MENA markets

    Format your response with these sections:
    # Outcome
    [Clear, concise results of your task]

    # Explanation
    [Detailed discussion of your process, research findings, and reasoning]

    # Resources Used
    [List of data sources, market benchmarks, and other references consulted]
    """

    # Step 1: Define Venture Description
    venture_definition_task = Task(
        description=f"""Define a clear, concise value proposition and description for the venture idea:

        Venture Idea: {venture_idea}

        Your task is to:
        1. Craft a one-sentence value proposition that clearly articulates the unique value of this venture
        2. Write a one-paragraph description (no revenue details)
        3. Research similar ventures in the GCC/MENA region to ensure market fit

        Ensure the description is specific to the GCC/MENA market context and highlights the venture's unique value.
        {negotiation_instructions}
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
        4. Research current monetization trends in the GCC/MENA digital market
        5. Consult with the Chief Strategy Officer if you need clarification on the venture's core value

        {negotiation_instructions}
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
        4. Research implementation costs for similar features in the GCC/MENA market
        5. Consult with the CTO about technical feasibility if needed

        {negotiation_instructions}
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
        4. Research actual revenue figures from similar ventures in the region
        5. Consult with the CMIO for market intelligence if needed

        {negotiation_instructions}
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
        4. Research actual development and operational costs in the GCC/MENA region
        5. Consult with the COO regarding operational requirements if needed

        {negotiation_instructions}
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
        5. Research success rates of similar monetization approaches in the region
        6. Consult with the CFO and CDAO to validate your ROI calculations

        {negotiation_instructions}
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
        3. Research successful MVP validation approaches in the GCC/MENA region
        4. Consult with the CXDO regarding user testing methodologies

        {negotiation_instructions}
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
        3. Research successful pivots by similar ventures in the GCC/MENA region
        4. Consult with the CSO regarding alignment with the original vision

        {negotiation_instructions}
        """,
        agent=cpno_agent,
        expected_output="Pivot implications for the top 3 streams",
        context=[venture_definition_task, prioritization_task, validation_strategy_task]
    )

    # Final Workshop Summary
    workshop_summary_task = Task(
        description=f"""Create a concise, actionable summary of the entire monetization workshop.

        Your task is to:
        1. Summarize the venture description in 1-2 sentences
        2. List the top 3 prioritized monetization streams with their key metrics:
           - Estimated monthly revenue
           - One-time development cost
           - Monthly OPEX
           - ROI
           - Validation approach
           - Pivot implications
        3. Provide final recommendations for which stream to pursue first and why
        4. Keep the summary to a single page (maximum 500 words)

        This summary should be immediately actionable for an early-stage venture in the GCC/MENA region.
        Focus on clarity, brevity, and actionable insights.

        {negotiation_instructions}
        """,
        agent=cso_agent,
        expected_output="Concise, actionable workshop summary with recommendations",
        context=[
            venture_definition_task,
            prioritization_task,
            validation_strategy_task,
            pivot_implications_task
        ]
    )

    # Comprehensive Workshop Documentation Task
    workshop_documentation_task = Task(
        description=f"""Document the entire workshop process, capturing key discussions, decisions, and insights.

        Your task is to:
        1. Observe and document each step of the workshop process
        2. Capture the key discussions, negotiations, and decision points between agents
        3. Document the research findings, market insights, and data sources used
        4. Create a cohesive narrative that shows the evolution of ideas throughout the workshop
        5. Highlight the reasoning behind major decisions

        For each workshop step, document:
        - The outcome (what was decided)
        - The explanation (how and why decisions were made)
        - The resources used (data sources, market benchmarks, etc.)
        - Any negotiations or discussions between agents

        Format your documentation with these sections:
        # Workshop Documentation

        ## Executive Summary
        [Brief overview of the entire workshop process and key outcomes]

        ## Step 1: Venture Definition
        ### Outcome
        [Clear description of the final venture definition]

        ### Explanation
        [How the definition was developed, including research and reasoning]

        ### Resources Used
        [Data sources and references consulted]

        [Continue with similar sections for each step of the workshop]

        ## Key Insights and Learnings
        [The most important takeaways from the workshop]

        {negotiation_instructions}
        """,
        agent=historian_agent,
        expected_output="Comprehensive documentation of the entire workshop process",
        context=[
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
        workshop_summary_task,
        workshop_documentation_task
    ]

    # Return all tasks
    return main_tasks
