from dotenv import load_dotenv
import os
import logging
from typing import Dict, Any, List

# Load environment variables
load_dotenv()

# Setup logging for configuration issues
logger = logging.getLogger(__name__)

class Config:
    """Enhanced configuration class with validation and error handling"""
    
    # Azure OpenAI Configuration
    OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
    OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    # Data paths
    DATA_PATH = os.getenv("DATA_PATH", "data")
    
    # File paths
    MEMBER_INFO_PATH = os.path.join(DATA_PATH, "member_info.json")
    PROCESSES_INFO_PATH = os.path.join(DATA_PATH, "processes.json")
    TECHSTACK_INFO_PATH = os.path.join(DATA_PATH, "techstack.json")
    CHAT_HISTORY_PATH = os.path.join(DATA_PATH, "chat_history.txt")
    
    # Application settings
    MAX_CONVERSATION_LENGTH = int(os.getenv("MAX_CONVERSATION_LENGTH", "50"))
    MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", "5000"))
    REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "30.0"))
    RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", "3"))
    
    # Logging configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "onboarding_assistant.log")
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate required configuration values"""
        required_configs = {
            'AZURE_OPENAI_ENDPOINT': cls.OPENAI_ENDPOINT,
            'AZURE_OPENAI_API_KEY': cls.OPENAI_API_KEY,
            'AZURE_OPENAI_DEPLOYMENT_NAME': cls.OPENAI_DEPLOYMENT_NAME
        }
        
        missing_configs: List[str] = []
        for key, value in required_configs.items():
            if not value:
                missing_configs.append(key)
        
        if missing_configs:
            logger.error(f"Missing required configuration: {', '.join(missing_configs)}")
            return False
        
        # Validate data directory exists
        if not os.path.exists(cls.DATA_PATH):
            try:
                os.makedirs(cls.DATA_PATH, exist_ok=True)
                logger.info(f"Created data directory: {cls.DATA_PATH}")
            except Exception as e:
                logger.error(f"Cannot create data directory {cls.DATA_PATH}: {e}")
                return False
        
        return True
    
    @classmethod
    def get_config_summary(cls) -> Dict[str, Any]:
        """Get a summary of current configuration (without sensitive data)"""
        return {
            "endpoint_configured": bool(cls.OPENAI_ENDPOINT),
            "api_key_configured": bool(cls.OPENAI_API_KEY),
            "deployment_configured": bool(cls.OPENAI_DEPLOYMENT_NAME),
            "api_version": cls.OPENAI_API_VERSION,
            "data_path": cls.DATA_PATH,
            "max_conversation_length": cls.MAX_CONVERSATION_LENGTH,
            "max_message_length": cls.MAX_MESSAGE_LENGTH,
            "request_timeout": cls.REQUEST_TIMEOUT,
            "retry_attempts": cls.RETRY_ATTEMPTS,
            "log_level": cls.LOG_LEVEL
        }
    
    @classmethod
    def check_data_files(cls) -> Dict[str, Any]:
        """Check if all required data files exist and are readable"""
        files_status = {}
        
        required_files = {
            "member_info": cls.MEMBER_INFO_PATH,
            "processes": cls.PROCESSES_INFO_PATH,
            "techstack": cls.TECHSTACK_INFO_PATH
        }
        
        for file_type, file_path in required_files.items():
            status = {
                "exists": os.path.exists(file_path),
                "readable": False,
                "size": 0,
                "path": file_path
            }
            
            if status["exists"]:
                try:
                    status["readable"] = os.access(file_path, os.R_OK)
                    status["size"] = os.path.getsize(file_path)
                except Exception as e:
                    logger.error(f"Error checking file {file_path}: {e}")
            
            files_status[file_type] = status
        
        return files_status
