from langchain.tools import tool
import json

@tool
def market_research_tool(query: str) -> str:
    """
    Research market data, trends, and benchmarks for the GCC/MENA region.
    
    Args:
        query: Specific market research question
        
    Returns:
        Market insights and data relevant to the query
    """
    # In a real implementation, this would connect to market research databases or APIs
    # For now, we'll return some sample data based on common queries
    
    gcc_market_data = {
        "digital adoption": "GCC digital adoption rates average 72% across the region, with UAE leading at 96%, followed by Saudi Arabia at 89%, Qatar at 86%, Bahrain at 78%, Kuwait at 72%, and Oman at 63%.",
        
        "e-commerce": "E-commerce penetration in GCC is approximately 65% with annual growth of 15-20%. Average order values range from $55-120 depending on category. Customer acquisition costs average $25-40 per customer.",
        
        "fintech": "Fintech adoption in GCC is growing at 30% annually. Payment processing fees range from 1.5-3.5%. Customer acquisition costs for fintech products average $30-60 per customer in the region.",
        
        "saas": "SaaS adoption in GCC businesses is approximately 45%, with 25-30% annual growth. Average contract values for B2B SaaS range from $3,000-15,000 annually. Sales cycles average 3-6 months.",
        
        "subscription": "Subscription model adoption in GCC is approximately 35% for digital services. Average monthly subscription values range from $10-25 for B2C and $50-500 for B2B services. Churn rates average 5-8% monthly.",
        
        "advertising": "Digital advertising CPM rates in GCC range from $2-8 depending on platform and targeting. Click-through rates average 0.5-2.5%. Conversion rates from ad click to purchase average 1.2-3.5%.",
        
        "marketplace": "Marketplace models in GCC typically charge 10-25% commission depending on category. Average customer acquisition costs range from $20-45. Retention rates after first purchase average 30-45%.",
        
        "b2b": "B2B sales cycles in GCC average 3-6 months. Customer acquisition costs range from $200-1,500 depending on sector. Average contract values range from $5,000-50,000 annually.",
        
        "b2c": "B2C customer acquisition costs in GCC range from $15-80 depending on sector. Conversion rates from website visit to purchase average 1.5-4%. Average customer lifetime value ranges from $100-500.",
        
        "mobile": "Mobile penetration in GCC exceeds 95%, with smartphone penetration at 85-92%. App download costs range from $1.50-4.00. In-app purchase conversion rates average 2-5%.",
        
        "ai": "AI adoption in GCC businesses is approximately 25%, with 40% annual growth. Implementation costs for basic AI solutions range from $20,000-100,000. ROI typically realized within 12-24 months.",
        
        "healthcare": "Digital healthcare adoption in GCC is growing at 25-30% annually. Telehealth consultation fees range from $30-150. Customer acquisition costs for health tech platforms average $50-120 per user.",
        
        "education": "EdTech adoption in GCC is growing at 20-25% annually. Average subscription values range from $15-50 monthly for B2C and $2,000-10,000 annually for B2B/institutional clients.",
        
        "real estate": "PropTech adoption in GCC is growing at 15-20% annually. Commission rates average 2-5% for sales and 5-10% for rentals. Customer acquisition costs range from $100-300 per lead.",
        
        "food delivery": "Food delivery penetration in GCC urban areas exceeds 70%. Commission rates range from 15-30%. Average order values range from $15-40. Customer acquisition costs average $20-50.",
        
        "logistics": "Last-mile delivery costs in GCC range from $5-15 per delivery. Fulfillment costs average $3-8 per order. Warehouse space costs $10-30 per square meter monthly depending on location.",
        
        "retail": "Retail customer acquisition costs in GCC range from $20-70. Conversion rates in physical stores average 20-30%, while e-commerce conversion rates average 1.5-4%. Average basket sizes range from $50-150.",
        
        "gaming": "Gaming market in GCC is growing at 25% annually. Average revenue per user (ARPU) ranges from $10-30 monthly. In-app purchase conversion rates average 3-7%. User acquisition costs range from $2-8.",
        
        "content": "Content subscription services in GCC have average monthly fees of $8-20. Churn rates average 4-7% monthly. Customer acquisition costs range from $25-60. Paid conversion rates from free to premium average 2-5%.",
        
        "enterprise": "Enterprise software adoption in GCC is growing at 15-20% annually. Average contract values range from $20,000-200,000 annually. Sales cycles average 6-12 months. Implementation costs typically add 20-40% to contract value."
    }
    
    # Check if any of the keywords are in the query
    for keyword, data in gcc_market_data.items():
        if keyword.lower() in query.lower():
            return f"GCC/MENA Market Data - {keyword.title()}: {data}"
    
    # Default response if no specific data is found
    return "No specific GCC/MENA market data found for this query. Consider refining your search terms to include specific business models or sectors like e-commerce, fintech, SaaS, subscription, advertising, marketplace, B2B, B2C, mobile, AI, healthcare, education, real estate, food delivery, logistics, retail, gaming, content, or enterprise."

@tool
def financial_modeling_tool(parameters: str) -> str:
    """
    Build financial models and ROI calculations for monetization streams.
    
    Args:
        parameters: JSON string containing financial parameters
        
    Returns:
        Financial projections and ROI analysis
    """
    try:
        params = json.loads(parameters)
        
        # Extract parameters with defaults
        one_time_cost = float(params.get("one_time_cost", 0))
        monthly_opex = float(params.get("monthly_opex", 0))
        monthly_revenue = float(params.get("monthly_revenue", 0))
        ramp_up_months = int(params.get("ramp_up_months", 6))
        time_horizon_months = int(params.get("time_horizon_months", 12))
        
        # Validate constraints
        if one_time_cost > 50000:
            return "ERROR: One-time cost exceeds $50K constraint for initial validation."
        
        if monthly_opex > 5000:
            return "ERROR: Monthly OPEX exceeds $5K constraint for initial validation."
        
        # Calculate financial metrics
        total_cost = one_time_cost + (monthly_opex * time_horizon_months)
        
        # Simple ramp-up model (linear)
        revenue = 0
        for month in range(1, time_horizon_months + 1):
            if month <= ramp_up_months:
                # During ramp-up, revenue grows linearly
                revenue_factor = month / ramp_up_months
            else:
                # After ramp-up, revenue is at 100%
                revenue_factor = 1.0
            
            revenue += monthly_revenue * revenue_factor
        
        # Calculate ROI
        roi = ((revenue - total_cost) / total_cost) * 100 if total_cost > 0 else 0
        
        # Calculate payback period (months)
        if monthly_revenue > monthly_opex:
            net_monthly = monthly_revenue - monthly_opex
            payback_months = one_time_cost / net_monthly if net_monthly > 0 else float('inf')
        else:
            payback_months = float('inf')
        
        # Format results
        result = {
            "one_time_cost": f"${one_time_cost:,.2f}",
            "monthly_opex": f"${monthly_opex:,.2f}",
            "monthly_revenue_at_scale": f"${monthly_revenue:,.2f}",
            "ramp_up_months": ramp_up_months,
            "total_cost_12_months": f"${total_cost:,.2f}",
            "total_revenue_12_months": f"${revenue:,.2f}",
            "roi_12_months": f"{roi:.2f}%",
            "payback_period_months": f"{payback_months:.1f}" if payback_months != float('inf') else "Never"
        }
        
        return json.dumps(result, indent=2)
    
    except Exception as e:
        return f"Error in financial modeling: {str(e)}"

@tool
def technical_assessment_tool(stream_description: str) -> str:
    """
    Assess technical feasibility and development costs for a monetization stream.
    
    Args:
        stream_description: Description of the monetization stream
        
    Returns:
        Technical assessment and cost estimates
    """
    # In a real implementation, this would use more sophisticated estimation models
    # For now, we'll provide a simple assessment based on keywords
    
    # Define complexity factors
    complexity_factors = {
        "payment": 3,
        "subscription": 2.5,
        "marketplace": 4,
        "ai": 3.5,
        "machine learning": 4,
        "analytics": 2,
        "dashboard": 2,
        "integration": 2.5,
        "api": 2,
        "mobile": 3,
        "app": 3,
        "web": 2,
        "platform": 3.5,
        "automation": 2.5,
        "blockchain": 4.5,
        "database": 2,
        "user authentication": 2,
        "social": 3,
        "content": 2,
        "video": 3.5,
        "audio": 3,
        "messaging": 3,
        "notification": 2,
        "recommendation": 3.5
    }
    
    # Calculate complexity score
    complexity_score = 1.0  # Base complexity
    matched_factors = []
    
    for factor, weight in complexity_factors.items():
        if factor.lower() in stream_description.lower():
            complexity_score += weight
            matched_factors.append(factor)
    
    # Cap complexity score
    complexity_score = min(complexity_score, 10.0)
    
    # Calculate cost estimates
    base_dev_cost = 5000  # Base development cost in USD
    dev_cost = base_dev_cost * complexity_score
    
    # Calculate monthly OPEX
    base_monthly_opex = 500  # Base monthly OPEX in USD
    monthly_opex = base_monthly_opex * (complexity_score / 2)
    
    # Estimate development time
    dev_time_weeks = complexity_score * 1.5
    
    # Prepare assessment
    assessment = {
        "complexity_score": f"{complexity_score:.1f}/10",
        "matched_complexity_factors": matched_factors,
        "estimated_development_cost": f"${dev_cost:,.2f}",
        "estimated_monthly_opex": f"${monthly_opex:,.2f}",
        "estimated_development_time": f"{dev_time_weeks:.1f} weeks",
        "technical_feasibility": "High" if complexity_score < 5 else "Medium" if complexity_score < 7.5 else "Low",
        "key_technical_components": [
            f"User interface development: ${dev_cost * 0.3:,.2f}",
            f"Backend development: ${dev_cost * 0.4:,.2f}",
            f"Integration work: ${dev_cost * 0.2:,.2f}",
            f"Testing and deployment: ${dev_cost * 0.1:,.2f}"
        ],
        "monthly_opex_breakdown": [
            f"Cloud infrastructure: ${monthly_opex * 0.4:,.2f}",
            f"Monitoring and maintenance: ${monthly_opex * 0.3:,.2f}",
            f"Third-party services: ${monthly_opex * 0.3:,.2f}"
        ]
    }
    
    return json.dumps(assessment, indent=2)

@tool
def validation_experiment_tool(stream_description: str) -> str:
    """
    Design validation experiments for monetization streams.
    
    Args:
        stream_description: Description of the monetization stream
        
    Returns:
        Validation experiment design
    """
    # Extract key aspects of the stream
    is_b2b = "b2b" in stream_description.lower() or "business" in stream_description.lower()
    is_subscription = "subscription" in stream_description.lower() or "recurring" in stream_description.lower()
    is_marketplace = "marketplace" in stream_description.lower() or "platform" in stream_description.lower()
    is_content = "content" in stream_description.lower() or "media" in stream_description.lower()
    is_service = "service" in stream_description.lower() or "consulting" in stream_description.lower()
    
    # Design appropriate validation approach
    if is_b2b:
        approach = "B2B Sales Validation"
        steps = [
            "Create a simple landing page with value proposition ($500-1,000)",
            "Develop a basic pitch deck and sales materials ($500-1,000)",
            "Conduct 15-20 customer discovery interviews ($2,000-3,000)",
            "Build a simplified demo or mockup ($5,000-10,000)",
            "Run 5-10 pilot proposals with potential customers ($3,000-5,000)"
        ]
        metrics = [
            "Number of meetings secured",
            "Conversion rate from meeting to pilot interest",
            "Willingness to pay (specific price points)",
            "Pilot conversion rate",
            "Feature priority feedback"
        ]
        timeline = "8-12 weeks"
        budget = "$15,000-25,000"
        
    elif is_marketplace:
        approach = "Marketplace MVP Validation"
        steps = [
            "Build a simple landing page for both sides of the marketplace ($1,000-2,000)",
            "Create manual matching process before building technology ($1,000-2,000)",
            "Recruit 10-20 supply-side participants ($3,000-5,000)",
            "Generate demand through targeted outreach ($5,000-8,000)",
            "Facilitate 20-30 transactions manually ($2,000-4,000)"
        ]
        metrics = [
            "Supply-side acquisition cost and conversion rate",
            "Demand-side acquisition cost and conversion rate",
            "Transaction completion rate",
            "User satisfaction scores (both sides)",
            "Repeat usage rates"
        ]
        timeline = "10-14 weeks"
        budget = "$20,000-30,000"
        
    elif is_subscription:
        approach = "Subscription Model Validation"
        steps = [
            "Create a landing page with subscription offering ($1,000-2,000)",
            "Build a minimum viable product with core features ($10,000-15,000)",
            "Set up payment processing for subscriptions ($1,000-2,000)",
            "Run targeted acquisition campaign ($5,000-8,000)",
            "Implement basic retention mechanisms ($2,000-4,000)"
        ]
        metrics = [
            "Visitor-to-signup conversion rate",
            "Signup-to-paid conversion rate",
            "Customer acquisition cost (CAC)",
            "30-day retention rate",
            "Feature usage patterns"
        ]
        timeline = "12-16 weeks"
        budget = "$25,000-35,000"
        
    elif is_content:
        approach = "Content Monetization Validation"
        steps = [
            "Produce 5-10 pieces of sample content ($3,000-5,000)",
            "Create a simple content delivery platform ($5,000-10,000)",
            "Implement basic paywall or monetization mechanism ($2,000-4,000)",
            "Run targeted promotion campaign ($5,000-8,000)",
            "Collect user feedback and usage data ($1,000-2,000)"
        ]
        metrics = [
            "Content engagement metrics (views, time spent)",
            "Conversion rate to paid/premium",
            "Willingness to pay for different content types",
            "Retention and repeat consumption",
            "Sharing and virality metrics"
        ]
        timeline = "8-12 weeks"
        budget = "$20,000-30,000"
        
    elif is_service:
        approach = "Service Offering Validation"
        steps = [
            "Define service packages and pricing ($500-1,000)",
            "Create service delivery process and templates ($2,000-4,000)",
            "Build a simple booking/request system ($5,000-8,000)",
            "Recruit initial service providers if needed ($3,000-5,000)",
            "Run limited-time promotion to acquire first customers ($5,000-8,000)"
        ]
        metrics = [
            "Lead-to-customer conversion rate",
            "Customer acquisition cost",
            "Service delivery cost",
            "Customer satisfaction scores",
            "Repeat purchase rate"
        ]
        timeline = "6-10 weeks"
        budget = "$15,000-25,000"
        
    else:
        approach = "General MVP Validation"
        steps = [
            "Create a landing page with clear value proposition ($1,000-2,000)",
            "Build a simplified version of the core offering ($10,000-15,000)",
            "Implement basic analytics and feedback collection ($1,000-2,000)",
            "Run targeted customer acquisition campaign ($5,000-8,000)",
            "Conduct user testing and interviews ($2,000-4,000)"
        ]
        metrics = [
            "Visitor-to-user conversion rate",
            "User engagement metrics",
            "Customer acquisition cost",
            "Feature usage patterns",
            "User satisfaction and feedback"
        ]
        timeline = "10-14 weeks"
        budget = "$20,000-30,000"
    
    # Compile validation plan
    validation_plan = {
        "validation_approach": approach,
        "key_steps": steps,
        "success_metrics": metrics,
        "estimated_timeline": timeline,
        "estimated_budget": budget,
        "critical_assumptions_to_test": [
            "Value proposition resonance with target market",
            "Willingness to pay at the proposed price point",
            "Cost of customer acquisition",
            "User engagement and retention",
            "Technical feasibility within budget constraints"
        ]
    }
    
    return json.dumps(validation_plan, indent=2)

@tool
def pivot_analysis_tool(parameters: str) -> str:
    """
    Analyze pivot implications for monetization streams.
    
    Args:
        parameters: JSON string containing pivot analysis parameters
        
    Returns:
        Pivot analysis and recommendations
    """
    try:
        params = json.loads(parameters)
        
        # Extract parameters
        original_description = params.get("original_description", "")
        stream_description = params.get("stream_description", "")
        
        # Analyze potential pivot dimensions
        pivot_dimensions = {
            "business_model": {
                "original": "",
                "new": "",
                "pivot_required": False
            },
            "target_market": {
                "original": "",
                "new": "",
                "pivot_required": False
            },
            "value_proposition": {
                "original": "",
                "new": "",
                "pivot_required": False
            },
            "revenue_model": {
                "original": "",
                "new": "",
                "pivot_required": False
            },
            "distribution_channel": {
                "original": "",
                "new": "",
                "pivot_required": False
            }
        }
        
        # Business model analysis
        if "b2b" in stream_description.lower() and "b2c" in original_description.lower():
            pivot_dimensions["business_model"]["original"] = "B2C"
            pivot_dimensions["business_model"]["new"] = "B2B"
            pivot_dimensions["business_model"]["pivot_required"] = True
        elif "b2c" in stream_description.lower() and "b2b" in original_description.lower():
            pivot_dimensions["business_model"]["original"] = "B2B"
            pivot_dimensions["business_model"]["new"] = "B2C"
            pivot_dimensions["business_model"]["pivot_required"] = True
        elif "b2g" in stream_description.lower() and "b2g" not in original_description.lower():
            pivot_dimensions["business_model"]["original"] = "B2B/B2C"
            pivot_dimensions["business_model"]["new"] = "B2G"
            pivot_dimensions["business_model"]["pivot_required"] = True
        
        # Revenue model analysis
        if "subscription" in stream_description.lower() and "subscription" not in original_description.lower():
            pivot_dimensions["revenue_model"]["original"] = "One-time/Transactional"
            pivot_dimensions["revenue_model"]["new"] = "Subscription"
            pivot_dimensions["revenue_model"]["pivot_required"] = True
        elif "transactional" in stream_description.lower() and "subscription" in original_description.lower():
            pivot_dimensions["revenue_model"]["original"] = "Subscription"
            pivot_dimensions["revenue_model"]["new"] = "Transactional"
            pivot_dimensions["revenue_model"]["pivot_required"] = True
        elif "freemium" in stream_description.lower() and "freemium" not in original_description.lower():
            pivot_dimensions["revenue_model"]["original"] = "Paid"
            pivot_dimensions["revenue_model"]["new"] = "Freemium"
            pivot_dimensions["revenue_model"]["pivot_required"] = True
        elif "marketplace" in stream_description.lower() and "marketplace" not in original_description.lower():
            pivot_dimensions["revenue_model"]["original"] = "Direct"
            pivot_dimensions["revenue_model"]["new"] = "Marketplace/Commission"
            pivot_dimensions["revenue_model"]["pivot_required"] = True
        
        # Distribution channel analysis
        if "direct" in stream_description.lower() and "partner" in original_description.lower():
            pivot_dimensions["distribution_channel"]["original"] = "Partner/Indirect"
            pivot_dimensions["distribution_channel"]["new"] = "Direct"
            pivot_dimensions["distribution_channel"]["pivot_required"] = True
        elif "partner" in stream_description.lower() and "partner" not in original_description.lower():
            pivot_dimensions["distribution_channel"]["original"] = "Direct"
            pivot_dimensions["distribution_channel"]["new"] = "Partner/Indirect"
            pivot_dimensions["distribution_channel"]["pivot_required"] = True
        
        # Count required pivots
        pivot_count = sum(1 for dim in pivot_dimensions.values() if dim["pivot_required"])
        
        # Determine pivot magnitude
        if pivot_count >= 3:
            pivot_magnitude = "Major"
        elif pivot_count >= 1:
            pivot_magnitude = "Moderate"
        else:
            pivot_magnitude = "Minor"
        
        # Generate adjusted description
        adjusted_description = original_description
        for dim in pivot_dimensions.values():
            if dim["pivot_required"]:
                # This is a simplistic approach - in a real implementation, 
                # we would use more sophisticated NLP to modify the description
                if dim["original"] in adjusted_description:
                    adjusted_description = adjusted_description.replace(dim["original"], dim["new"])
        
        # Compile pivot analysis
        pivot_analysis = {
            "pivot_magnitude": pivot_magnitude,
            "pivot_dimensions": pivot_dimensions,
            "pivot_count": pivot_count,
            "adjusted_description": adjusted_description,
            "key_implications": [
                f"Business model changes: {pivot_dimensions['business_model']['new'] if pivot_dimensions['business_model']['pivot_required'] else 'No change required'}",
                f"Target market changes: {pivot_dimensions['target_market']['new'] if pivot_dimensions['target_market']['pivot_required'] else 'No change required'}",
                f"Revenue model changes: {pivot_dimensions['revenue_model']['new'] if pivot_dimensions['revenue_model']['pivot_required'] else 'No change required'}",
                f"Distribution changes: {pivot_dimensions['distribution_channel']['new'] if pivot_dimensions['distribution_channel']['pivot_required'] else 'No change required'}"
            ],
            "implementation_considerations": [
                "Team skill alignment with new direction",
                "Technology stack implications",
                "Go-to-market strategy adjustments",
                "Funding requirements for the pivot",
                "Timeline implications"
            ]
        }
        
        return json.dumps(pivot_analysis, indent=2)
    
    except Exception as e:
        return f"Error in pivot analysis: {str(e)}"
