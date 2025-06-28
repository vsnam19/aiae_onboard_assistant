from dotenv import load_dotenv
import os


load_dotenv()

# Configuration for the application
class Config:
    OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
    OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    DATA_PATH = "data"
    
    MEMBER_INFO_PATH = os.path.join(DATA_PATH, "member_info.json")
    PROCESSES_INFO_PATH = os.path.join(DATA_PATH, "processes.json")
    TECHSTACK_INFO_PATH = os.path.join(DATA_PATH, "techstack.json")
    CHAT_HISTORY_PATH = os.path.join(DATA_PATH, "chat_history.txt")