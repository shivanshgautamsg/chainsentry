from dotenv import load_dotenv
import os

load_dotenv()

print("API Key:", os.getenv("NVD_API_KEY"))
