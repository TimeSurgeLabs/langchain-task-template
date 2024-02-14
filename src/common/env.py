import os

from dotenv import load_dotenv

# environment variables, like configuration, api keys, etc.

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORGANIZATION = os.getenv("OPENAI_ORGANIZATION")
