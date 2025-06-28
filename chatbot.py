from typing import List, Dict, Any, Optional, Tuple
from openai import AzureOpenAI
from config import Config
from prompt import Prompt
import json
import logging
import traceback
import time
from datetime import datetime
import os

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential
)

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
    handlers=[
        logging.FileHandler('onboarding_assistant.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class FileNotFoundError(Exception):
    """Custom exception for missing data files"""
    pass


class DataValidationError(Exception):
    """Custom exception for invalid data format"""
    pass


class APIConnectionError(Exception):
    """Custom exception for API connection issues"""
    pass


def validate_json_structure(data: Any, expected_keys: List[str], context: str) -> bool:
    """Validate JSON data structure"""
    try:
        if not isinstance(data, list):
            raise DataValidationError(
                f"{context}: Expected list, got {type(data)}")

        for item in data:
            if not isinstance(item, dict):
                raise DataValidationError(
                    f"{context}: Expected dict items, got {type(item)}")

            missing_keys = [key for key in expected_keys if key not in item]
            if missing_keys:
                logger.warning(
                    f"{context}: Missing keys {missing_keys} in item")

        return True
    except Exception as e:
        logger.error(f"Data validation failed for {context}: {str(e)}")
        return False


def get_member_information() -> str:
    """Load member information from JSON file with  error handling."""
    try:
        file_path = Config.MEMBER_INFO_PATH

        # Check file existence
        if not os.path.exists(file_path):
            error_msg = f"Member information file not found at: {file_path}"
            logger.error(error_msg)
            return json.dumps({
                "error": "Data temporarily unavailable",
                "message": "Member information is currently being updated. Please try again in a few minutes or contact IT support.",
                "contact": "IT Support: it-support@company.com"
            }, indent=2)

        # Check file permissions
        if not os.access(file_path, os.R_OK):
            error_msg = f"Cannot read member information file: {file_path}"
            logger.error(error_msg)
            return json.dumps({
                "error": "Access denied",
                "message": "Unable to access member information. Please contact IT support.",
                "contact": "IT Support: it-support@company.com"
            }, indent=2)

        # Load and validate data
        with open(file_path, 'r', encoding='utf-8') as file:
            member_info = json.load(file)

        # Validate data structure
        expected_keys = ['project_code', 'project_name', 'members']
        if not validate_json_structure(member_info, expected_keys, "Member Information"):
            logger.warning(
                "Member information has unexpected structure but proceeding")

        logger.info(
            f"Successfully loaded member information: {len(member_info)} projects")
        return json.dumps(member_info, indent=2, ensure_ascii=False)

    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON format in member information file: {str(e)}"
        logger.error(error_msg)
        return json.dumps({
            "error": "Data format error",
            "message": "Member information file has formatting issues. IT has been notified.",
            "contact": "For immediate assistance: hr@company.com"
        }, indent=2)

    except PermissionError:
        error_msg = "Permission denied accessing member information file"
        logger.error(error_msg)
        return json.dumps({
            "error": "Access denied",
            "message": "Unable to access member information. Please contact IT support.",
            "contact": "IT Support: it-support@company.com"
        }, indent=2)

    except Exception as e:
        error_msg = f"Unexpected error loading member information: {str(e)}"
        logger.error(error_msg)
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return json.dumps({
            "error": "System error",
            "message": "An unexpected error occurred. Please try again or contact support.",
            "contact": "Support: support@company.com"
        }, indent=2)


def get_process_information() -> str:
    """Load process information from JSON file with  error handling."""
    try:
        file_path = Config.PROCESSES_INFO_PATH

        if not os.path.exists(file_path):
            error_msg = f"Process information file not found at: {file_path}"
            logger.error(error_msg)
            return json.dumps({
                "error": "Data temporarily unavailable",
                "message": "Process information is currently being updated. Please try again later.",
                "alternative": "For urgent process questions, contact your manager or team lead."
            }, indent=2)

        with open(file_path, 'r', encoding='utf-8') as file:
            processes_info = json.load(file)

        # Validate data structure
        expected_keys = ['project_code', 'project_name', 'processes']
        validate_json_structure(
            processes_info, expected_keys, "Process Information")

        logger.info(
            f"Successfully loaded process information: {len(processes_info)} projects")
        return json.dumps(processes_info, indent=2, ensure_ascii=False)

    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON in process information file: {str(e)}"
        logger.error(error_msg)
        return json.dumps({
            "error": "Data format error",
            "message": "Process information file has formatting issues. Please contact your team lead for process details.",
            "contact": "Team Lead or Manager"
        }, indent=2)

    except Exception as e:
        error_msg = f"Unexpected error loading process information: {str(e)}"
        logger.error(error_msg)
        return json.dumps({
            "error": "System error",
            "message": "Unable to load process information. Please contact your manager for workflow details.",
            "contact": "Manager or Team Lead"
        }, indent=2)


def get_techstack_information() -> str:
    """Load tech stack information from JSON file with  error handling."""
    try:
        file_path = Config.TECHSTACK_INFO_PATH

        if not os.path.exists(file_path):
            error_msg = f"Tech stack information file not found at: {file_path}"
            logger.error(error_msg)
            return json.dumps({
                "error": "Data temporarily unavailable",
                "message": "Technology stack information is currently being updated.",
                "alternative": "Please ask your team lead about the specific technologies used in your project."
            }, indent=2)

        with open(file_path, 'r', encoding='utf-8') as file:
            techstack_info = json.load(file)

        # Validate data structure
        expected_keys = ['project_code', 'project_name', 'tech_stack']
        validate_json_structure(
            techstack_info, expected_keys, "Tech Stack Information")

        logger.info(
            f"Successfully loaded tech stack information: {len(techstack_info)} projects")
        return json.dumps(techstack_info, indent=2, ensure_ascii=False)

    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON in tech stack information file: {str(e)}"
        logger.error(error_msg)
        return json.dumps({
            "error": "Data format error",
            "message": "Technology information file has formatting issues. Please ask your team about the tech stack.",
            "contact": "Team Lead or Senior Developer"
        }, indent=2)

    except Exception as e:
        error_msg = f"Unexpected error loading tech stack information: {str(e)}"
        logger.error(error_msg)
        return json.dumps({
            "error": "System error",
            "message": "Unable to load technology information. Please contact your team for tech stack details.",
            "contact": "Team Lead or Technical Manager"
        }, indent=2)


def get_user_project_assignment(user_name: str, user_department: str = None) -> str:
    """Find user's project assignment with enhanced search and error handling."""
    try:
        # Validate input
        if not user_name or not user_name.strip():
            return json.dumps({
                'user_found': False,
                'error': 'Please provide a valid name to search for project assignments.',
                'suggestion': 'Enter your full name as it appears in company records.'
            }, indent=2)

        user_name = user_name.strip()
        file_path = Config.MEMBER_INFO_PATH

        if not os.path.exists(file_path):
            return json.dumps({
                'user_found': False,
                'error': 'Member information is temporarily unavailable.',
                'suggestion': 'Please contact HR at hr@company.com for your project assignment.'
            }, indent=2)

        with open(file_path, 'r', encoding='utf-8') as file:
            member_info = json.load(file)

        user_projects = []
        search_variations = [
            user_name.lower(),
            user_name.lower().split()[
                0] if ' ' in user_name else user_name.lower(),  # First name
            ' '.join(user_name.lower().split()[:2]) if len(
                user_name.split()) > 1 else user_name.lower()  # First + Last
        ]

        # Enhanced search through all projects
        for project in member_info:
            if not isinstance(project, dict) or 'members' not in project:
                continue

            for member in project.get('members', []):
                if not isinstance(member, dict):
                    continue

                member_name = member.get('name', '').lower()

                # Multiple matching strategies
                name_match = any(
                    search_var in member_name or
                    member_name.startswith(search_var) or
                    any(search_var in name_part for name_part in member_name.split())
                    for search_var in search_variations
                )

                if name_match:
                    # Additional department filter if provided
                    if user_department:
                        member_dept = member.get('department', '').lower()
                        if user_department.lower() not in member_dept:
                            continue

                    user_projects.append({
                        'project_code': project.get('project_code'),
                        'project_name': project.get('project_name'),
                        'department': project.get('department'),
                        'status': project.get('status'),
                        'description': project.get('description'),
                        'member_info': {
                            'employee_id': member.get('employee_id'),
                            'name': member.get('name'),
                            'role': member.get('role'),
                            'email': member.get('email'),
                            'team': member.get('team'),
                            'manager': member.get('manager'),
                            'hire_date': member.get('hire_date'),
                            'status': member.get('status'),
                            'department': member.get('department')
                        }
                    })

        if user_projects:
            result = {
                'user_found': True,
                'total_projects': len(user_projects),
                'search_name': user_name,
                'projects': user_projects,
                'message': f"Found {len(user_projects)} project assignment(s) for {user_name}"
            }
        else:
            # Provide helpful suggestions when user not found
            result = {
                'user_found': False,
                'search_name': user_name,
                'message': f"No project assignment found for: {user_name}",
                'suggestions': [
                    "Check if your name is spelled exactly as in company records",
                    "Try using just your first name",
                    "Contact HR if you're a very recent hire",
                    "Verify with your hiring manager about project assignments"
                ],
                'contacts': {
                    'hr': 'hr@company.com',
                    'it_support': 'it-support@company.com'
                }
            }

        logger.info(
            f"User project lookup for '{user_name}': {len(user_projects)} projects found")
        return json.dumps(result, indent=2, ensure_ascii=False)

    except json.JSONDecodeError as e:
        error_msg = f"Data format error in member information: {str(e)}"
        logger.error(error_msg)
        return json.dumps({
            'user_found': False,
            'error': 'Member information file has formatting issues.',
            'suggestion': 'Please contact HR at hr@company.com for your project assignment.'
        }, indent=2)

    except Exception as e:
        error_msg = f"Error looking up user project assignment: {str(e)}"
        logger.error(error_msg)
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return json.dumps({
            'user_found': False,
            'error': 'System error occurred during lookup.',
            'suggestion': 'Please try again or contact support@company.com'
        }, indent=2)


class AzureOpenAIClient:
    _instance: Optional[AzureOpenAI] = None
    _last_request_time: float = 0
    # Minimum time between requests (rate limiting)
    _min_request_interval: float = 0.1

    @staticmethod
    def get_instance() -> AzureOpenAI:
        """Get or create singleton instance of Azure OpenAI client with validation."""
        if AzureOpenAIClient._instance is None:
            # Validate all required configurations
            required_configs = {
                'OPENAI_ENDPOINT': Config.OPENAI_ENDPOINT,
                'OPENAI_API_KEY': Config.OPENAI_API_KEY,
                'OPENAI_API_VERSION': Config.OPENAI_API_VERSION,
                'OPENAI_DEPLOYMENT_NAME': Config.OPENAI_DEPLOYMENT_NAME
            }

            missing_configs = [key for key,
                               value in required_configs.items() if not value]
            if missing_configs:
                error_msg = f"Missing Azure OpenAI configuration: {', '.join(missing_configs)}"
                logger.error(error_msg)
                raise APIConnectionError(error_msg)

            try:
                AzureOpenAIClient._instance = AzureOpenAI(
                    azure_endpoint=Config.OPENAI_ENDPOINT,
                    api_key=Config.OPENAI_API_KEY,
                    api_version=Config.OPENAI_API_VERSION
                )
                logger.info("Azure OpenAI client initialized successfully")
            except Exception as e:
                error_msg = f"Failed to initialize Azure OpenAI client: {str(e)}"
                logger.error(error_msg)
                raise APIConnectionError(error_msg)

        return AzureOpenAIClient._instance

    @staticmethod
    def _apply_rate_limiting():
        """Apply rate limiting between requests."""
        current_time = time.time()
        time_since_last_request = current_time - AzureOpenAIClient._last_request_time

        if time_since_last_request < AzureOpenAIClient._min_request_interval:
            sleep_time = AzureOpenAIClient._min_request_interval - time_since_last_request
            time.sleep(sleep_time)

        AzureOpenAIClient._last_request_time = time.time()

    @staticmethod
    def get_chat_completion(
        messages: List[Dict[str, Any]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
        tools: Optional[List[Dict[str, Any]]] = None,
        max_retries: int = 3
    ) -> Optional[Any]:
        """Get chat completion with  error handling and retries."""

        # Validate inputs
        if not messages:
            logger.error("Messages list cannot be empty")
            return None

        if len(messages) > 50:  # Reasonable conversation length limit
            logger.warning(f"Very long conversation: {len(messages)} messages")

        client = AzureOpenAIClient.get_instance()

        for attempt in range(max_retries):
            try:
                # Apply rate limiting
                AzureOpenAIClient._apply_rate_limiting()

                # Prepare request parameters
                request_params = {
                    "model": Config.OPENAI_DEPLOYMENT_NAME,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }

                # Add tools if provided
                if tools:
                    request_params["tools"] = tools
                    request_params["tool_choice"] = "auto"

                logger.info(
                    f"Making API request (attempt {attempt + 1}/{max_retries}) with {len(messages)} messages")

                start_time = time.time()
                response = client.chat.completions.create(**request_params)
                response_time = time.time() - start_time

                logger.info(
                    f"Successfully received response from Azure OpenAI (took {response_time:.2f}s)")
                return response

            except Exception as e:
                error_msg = f"API request failed (attempt {attempt + 1}/{max_retries}): {str(e)}"
                logger.error(error_msg)

                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(
                        f"All {max_retries} attempts failed. Full traceback: {traceback.format_exc()}")
                    return None


class OnboardingAssistant:
    def __init__(self):
        """Initialize the enhanced OnboardingAssistant."""
        self.system_prompt = Prompt.SYSTEM_PROMPT
        self.conversation_history: List[Dict[str, Any]] = []
        self.chat_history_file = Config.CHAT_HISTORY_PATH
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Enhanced function definitions with better error handling
        self.function_definitions = [
            {
                "type": "function",
                "function": {
                    "name": "get_member_information",
                    "description": """Retrieve team member information organized by projects. 
                    
                    Returns: JSON with project details and member lists including names, roles, emails, departments, teams, managers, hire dates, skills, status, phone, and location.
                    
                    Use for: team structure questions, contact information, role inquiries, project assignments, "who works on X", "what's John's role", "team composition".""",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_process_information",
                    "description": """Retrieve company processes and workflows organized by projects.
                    
                    Returns: JSON with project processes including process names, descriptions, status, dates, responsible members, deliverables, dependencies, and progress percentages.
                    
                    Use for: workflow questions, process status inquiries, timeline questions, responsibility clarification, "how do we do X", "what's the status of Y", "who handles Z".""",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_techstack_information",
                    "description": """Retrieve technology stack information organized by projects.
                    
                    Returns: JSON with project tech stacks including frontend, backend, database, AI/ML, cloud technologies, and tools with versions, purposes, status, documentation URLs, support teams, and learning resources.
                    
                    Use for: technology questions, tool information, version details, documentation links, "what tech do we use", "which database", "where to learn React", "what's our cloud setup".""",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_user_project_assignment",
                    "description": """Find a specific user's project assignment(s) based on their name and optional department filter.
                    
                    Returns: JSON with user_found status, total projects count, and detailed project assignments including project codes, names, departments, status, descriptions, and member information.
                    
                    Use for: personal project assignment queries, checking current projects, "what project am I assigned to", "which team am I in", "who is my manager".""",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_name": {"type": "string", "description": "The full name or first name of the user to look up"},
                            "user_department": {"type": "string", "description": "Optional department filter (Engineering, Product, Design, etc.)"}
                        },
                        "required": ["user_name"]
                    }
                }
            }
        ]

        # Function mapping for execution
        self.function_map = {
            "get_member_information": get_member_information,
            "get_process_information": get_process_information,
            "get_techstack_information": get_techstack_information,
            "get_user_project_assignment": get_user_project_assignment
        }

        self.reset_conversation()
        logger.info(
            f"OnboardingAssistant initialized successfully (Session: {self.session_id})")

    def save_conversation_history(self, role: str, content: str):
        """Save conversation history with session tracking."""
        try:
            os.makedirs(os.path.dirname(self.chat_history_file), exist_ok=True)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_entry = f"[{timestamp}] [{self.session_id}] {role}: {content}\n"

            with open(self.chat_history_file, 'a', encoding='utf-8') as file:
                file.write(formatted_entry)

            logger.debug("Conversation history saved successfully")
        except Exception as e:
            logger.error(f"Error saving conversation history: {str(e)}")

    def clear_conversation_history(self):
        """Clear conversation history file safely."""
        try:
            if os.path.exists(self.chat_history_file):
                with open(self.chat_history_file, 'w', encoding='utf-8') as file:
                    file.write(
                        f"# Conversation history cleared at {datetime.now()}\n")
            logger.info("Conversation history cleared successfully")
        except Exception as e:
            logger.error(f"Error clearing conversation history: {str(e)}")

    def set_additional_context(self, context: str):
        """Set additional context with validation."""
        if not context or not context.strip():
            logger.warning("No valid context provided")
            return False

        context = context.strip()
        self.conversation_history.append({
            "role": "user",
            "content": f"[CONTEXT] {context}"
        })
        logger.info(f"Additional context set: {context[:100]}...")
        return True

    def reset_conversation(self):
        """Reset conversation with prompts."""
        self.conversation_history = [
            {"role": "system", "content": self.system_prompt}
        ]

        # Add few-shot examples
        self.conversation_history.extend(Prompt.FEW_SHOT_EXAMPLES)
        self.clear_conversation_history()
        logger.info("Conversation history reset with prompts")

    def _validate_input(self, user_message: str) -> Tuple[bool, str]:
        """Enhanced input validation with specific error messages."""
        if not user_message:
            return False, "Please enter a message."

        message = user_message.strip()
        if not message:
            return False, "Please enter a non-empty message."

        if len(message) > 5000:  # Reasonable limit
            return False, "Message is too long. Please keep it under 5000 characters."

        # Check for potentially problematic content
        if message.count('\n') > 50:  # Too many line breaks
            return False, "Message has too many line breaks. Please format it more concisely."

        return True, ""

    def _handle_tool_calls(self, response) -> str:
        """Enhanced tool call handling with better error recovery."""
        try:
            tool_calls = response.choices[0].message.tool_calls
            if not tool_calls:
                logger.warning("No tool calls found in response")
                return "I need to look up some information but encountered an issue. Please try rephrasing your question."

            # Add assistant message with tool calls
            assistant_message = {
                "role": "assistant",
                "content": response.choices[0].message.content,
                "tool_calls": []
            }

            # Process each tool call
            for tool_call in tool_calls:
                assistant_message["tool_calls"].append({
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                })

            self.conversation_history.append(assistant_message)

            # Execute functions and collect results
            results = []
            for tool_call in tool_calls:
                function_name = tool_call.function.name

                if function_name in self.function_map:
                    try:
                        # Parse arguments if provided
                        if tool_call.function.arguments:
                            try:
                                args = json.loads(tool_call.function.arguments)
                                if function_name == "get_user_project_assignment":
                                    function_result = self.function_map[function_name](
                                        **args)
                                else:
                                    function_result = self.function_map[function_name](
                                    )
                            except json.JSONDecodeError:
                                function_result = self.function_map[function_name](
                                )
                        else:
                            function_result = self.function_map[function_name](
                            )

                        logger.info(
                            f"Successfully executed function: {function_name}")
                        results.append(function_result)

                    except Exception as e:
                        error_msg = f"Error executing {function_name}: {str(e)}"
                        logger.error(error_msg)
                        results.append(json.dumps({
                            "error": "Function execution failed",
                            "message": "Unable to retrieve information at this time. Please try again later.",
                            "function": function_name
                        }, indent=2))
                else:
                    error_msg = f"Unknown function call: {function_name}"
                    logger.error(error_msg)
                    results.append(json.dumps({
                        "error": "Unknown function",
                        "message": "The requested operation is not available.",
                        "function": function_name
                    }, indent=2))

                # Add tool response
                self.conversation_history.append({
                    "role": "tool",
                    "content": str(results[-1]),
                    "tool_call_id": tool_call.id
                })

            return "\n".join(results) if len(results) > 1 else results[0]

        except Exception as e:
            error_msg = f"Error handling tool calls: {str(e)}"
            logger.error(error_msg)
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return "I encountered an error while looking up information. Please try your question again."

    def _get_final_response(self) -> str:
        """Generate final response with fallback handling."""
        try:
            follow_up_response = AzureOpenAIClient.get_chat_completion(
                self.conversation_history,
                max_tokens=1500,  # Allow longer responses for  answers
                temperature=0.7
            )

            if (follow_up_response and
                follow_up_response.choices and
                    follow_up_response.choices[0].message.content):

                final_response = follow_up_response.choices[0].message.content
                self.conversation_history.append({
                    "role": "assistant",
                    "content": final_response
                })
                logger.info("Final response generated successfully")
                return final_response
            else:
                logger.warning("No follow-up response generated")
                # Try to provide a helpful fallback based on the tool results
                last_tool_result = None
                for msg in reversed(self.conversation_history):
                    if msg.get("role") == "tool":
                        last_tool_result = msg.get("content")
                        break

                if last_tool_result:
                    return "I've retrieved the information you requested. Here are the details:\n\n" + last_tool_result
                else:
                    return "I've looked up the information but couldn't format a proper response. Please try rephrasing your question."

        except Exception as e:
            error_msg = f"Error generating final response: {str(e)}"
            logger.error(error_msg)
            return "I found some information but encountered an error while formatting the response. Please try asking your question again."

    def send_message(self, user_message: str) -> str:
        """Public interface for sending messages with full error handling."""
        try:
            self.save_conversation_history("user", user_message)
            response = self.__send_message(user_message)
            self.save_conversation_history("assistant", response)
            return response
        except Exception as e:
            error_msg = f"Critical error in send_message: {str(e)}"
            logger.error(error_msg)
            return "I'm experiencing technical difficulties. Please try again in a moment."

    @retry(wait=wait_random_exponential(min=5, max=60), stop=stop_after_attempt(5))
    def __send_message(self, user_message: str) -> str:
        """Internal message processing with  error handling."""
        try:
            # Validate input
            is_valid, error_message = self._validate_input(user_message)
            if not is_valid:
                return error_message

            # Add user message to conversation
            self.conversation_history.append({
                "role": "user",
                "content": user_message.strip()
            })
            logger.info(f"Processing user message: {user_message[:100]}...")

            # Get initial response from AI
            response = AzureOpenAIClient.get_chat_completion(
                self.conversation_history,
                tools=self.function_definitions,
                max_tokens=1500,
                temperature=0.7
            )

            if response is None:
                logger.error("No response from Azure OpenAI")
                self.conversation_history.pop()  # Remove user message
                return "I'm having trouble connecting to my knowledge base right now. Please try again in a few moments."

            # Process response based on type
            if (response.choices and response.choices[0].message.tool_calls):
                logger.info("Processing function call(s)")
                self._handle_tool_calls(response)
                return self._get_final_response()
            else:
                # Direct response without function calls
                if (response.choices and response.choices[0].message.content):
                    content = response.choices[0].message.content
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": content
                    })
                    logger.info("Direct response processed successfully")
                    return content
                else:
                    logger.warning("No content in response")
                    self.conversation_history.pop()  # Remove user message
                    return "I didn't receive a proper response. Please try rephrasing your question."

        except APIConnectionError as e:
            logger.error(f"API connection error: {str(e)}")
            if self.conversation_history and self.conversation_history[-1]["role"] == "user":
                self.conversation_history.pop()
            return "I'm having trouble connecting to my AI service. Please check your internet connection and try again."

        except Exception as e:
            error_msg = f"Unexpected error in __send_message: {str(e)}"
            logger.error(error_msg)
            logger.error(f"Full traceback: {traceback.format_exc()}")

            # Clean up conversation history
            if self.conversation_history and self.conversation_history[-1]["role"] == "user":
                self.conversation_history.pop()

            return "I encountered an unexpected error. Please try again with a different question."

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get conversation history with safe copying."""
        try:
            return [msg.copy() for msg in self.conversation_history]
        except Exception as e:
            logger.error(f"Error getting conversation history: {str(e)}")
            return []

    def get_conversation_length(self) -> int:
        """Get conversation length safely."""
        try:
            return len(self.conversation_history)
        except Exception as e:
            logger.error(f"Error getting conversation length: {str(e)}")
            return 0

    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get detailed conversation summary."""
        try:
            user_messages = [
                msg for msg in self.conversation_history if msg["role"] == "user"]
            assistant_messages = [
                msg for msg in self.conversation_history if msg["role"] == "assistant"]
            tool_messages = [
                msg for msg in self.conversation_history if msg["role"] == "tool"]

            return {
                "session_id": self.session_id,
                "total_messages": len(self.conversation_history),
                "user_messages": len(user_messages),
                "assistant_messages": len(assistant_messages),
                "tool_calls": len(tool_messages),
                "conversation_started": len(self.conversation_history) > 1,
                "last_activity": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            logger.error(f"Error generating conversation summary: {str(e)}")
            return {"error": "Unable to generate summary"}
