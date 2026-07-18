import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Model Configuration
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

# Report Configuration
MAX_RESULTS = 3
TEMPERATURE = 0
MAX_WEB_RESULTS = 3
MAX_ARXIV_RESULTS = 3
REPORT_FORMAT = "pdf"

# Validate required environment variables
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing in the .env file.")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is missing in the .env file.")