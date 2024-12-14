import os
from dotenv import load_dotenv

load_dotenv()

PAGESPEED_API_KEY = os.getenv("PAGESPEED_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
