# OpenAI model to use
OPENAI_MODEL = "gpt-4.1"  # Using the latest GPT-4.1 model

# Alternative models
OPENAI_MODEL_MINI = "gpt-4.1-mini"  # More affordable option if needed

# GCC/MENA Market Constants
GCC_COUNTRIES = ["UAE", "Saudi Arabia", "Qatar", "Kuwait", "Bahrain", "Oman"]
MENA_COUNTRIES = GCC_COUNTRIES + ["Egypt", "Jordan", "Lebanon", "Morocco", "Tunisia"]

# Funding Constraints
MAX_VALIDATION_BUDGET = 50000  # $50K for initial validation
MAX_PRESEED_BUDGET = 250000  # $250K for pre-seed
MAX_MONTHLY_OPEX = 5000  # $5K/month OPEX limit

# Workshop Configuration
WORKSHOP_STEPS = [
    "Venture Definition",
    "High-Level Streams",
    "Detailed Streams",
    "Stream Prioritization",
    "Validation Strategy",
    "Pivot Implications"
]

# Agent Configuration
AGENT_TEMPERATURE = 0.2  # Lower temperature for more conservative estimates
