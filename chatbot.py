from typing import List, Dict, Any, Optional
from openai import AzureOpenAI
from config import Config
from prompt import Prompt
import json
import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_member_information() -> str:
    """Load member information from JSON file with improved error handling."""
    try:
        with open(Config.MEMBER_INFO_PATH, 'r', encoding='utf-8') as file:
            member_info = json.load(file)
        logger.info("Successfully loaded member information")
        return json.dumps(member_info, indent=2, ensure_ascii=False)
    except FileNotFoundError:
        error_msg = f"Member information file not found at: {Config.MEMBER_INFO_PATH}"
        logger.error(error_msg)
        return error_msg
    except json.JSONDecodeError as e:
        error_msg = f"Error decoding JSON from member information file: {str(e)}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Unexpected error loading member information: {str(e)}"
        logger.error(error_msg)
        return error_msg

def get_process_information() -> str:
    """Load process information from JSON file with improved error handling."""
    try:
        with open(Config.PROCESSES_INFO_PATH, 'r', encoding='utf-8') as file:
            processes_info = json.load(file)
        logger.info("Successfully loaded process information")
        return json.dumps(processes_info, indent=2, ensure_ascii=False)
    except FileNotFoundError:
        error_msg = f"Process information file not found at: {Config.PROCESSES_INFO_PATH}"
        logger.error(error_msg)
        return error_msg
    except json.JSONDecodeError as e:
        error_msg = f"Error decoding JSON from process information file: {str(e)}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Unexpected error loading process information: {str(e)}"
        logger.error(error_msg)
        return error_msg

def get_techstack_information() -> str:
    """Load tech stack information from JSON file with improved error handling."""
    try:
        with open(Config.TECHSTACK_INFO_PATH, 'r', encoding='utf-8') as file:
            techstack_info = json.load(file)
        logger.info("Successfully loaded tech stack information")
        return json.dumps(techstack_info, indent=2, ensure_ascii=False)
    except FileNotFoundError:
        error_msg = f"Tech stack information file not found at: {Config.TECHSTACK_INFO_PATH}"
        logger.error(error_msg)
        return error_msg
    except json.JSONDecodeError as e:
        error_msg = f"Error decoding JSON from tech stack information file: {str(e)}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Unexpected error loading tech stack information: {str(e)}"
        logger.error(error_msg)
        return error_msg

def get_user_project_assignment(user_name: str, user_department: str = None) -> str:
    """Find the current user's specific project assignment(s)."""
    try:
        with open(Config.MEMBER_INFO_PATH, 'r', encoding='utf-8') as file:
            member_info = json.load(file)
        
        user_projects = []
        
        # Search through all projects for the user
        for project in member_info:
            for member in project.get('members', []):
                # Match by name (flexible matching)
                member_name = member.get('name', '').lower()
                search_name = user_name.lower()
                
                # Check if it's a match (first name, full name, or partial match)
                if (search_name in member_name or 
                    member_name.startswith(search_name) or
                    any(search_name in name_part for name_part in member_name.split())):
                    
                    # Additional department check if provided
                    if user_department and member.get('department'):
                        if user_department.lower() not in member.get('department', '').lower():
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
                            'status': member.get('status')
                        }
                    })
        
        if user_projects:
            result = {
                'user_found': True,
                'total_projects': len(user_projects),
                'projects': user_projects
            }
        else:
            result = {
                'user_found': False,
                'message': f"No project assignment found for user: {user_name}" + 
                          (f" in department: {user_department}" if user_department else ""),
                'suggestion': "Please check with HR or your manager for project assignment details."
            }
        
        logger.info(f"User project lookup for '{user_name}': {len(user_projects)} projects found")
        return json.dumps(result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        error_msg = f"Error looking up user project assignment: {str(e)}"
        logger.error(error_msg)
        return json.dumps({
            'user_found': False,
            'error': error_msg
        }, indent=2)

class AzureOpenAIClient:
    _instance: Optional[AzureOpenAI] = None

    @staticmethod
    def get_instance() -> AzureOpenAI:
        """Get or create singleton instance of Azure OpenAI client."""
        if AzureOpenAIClient._instance is None:
            if not all([Config.OPENAI_ENDPOINT, Config.OPENAI_API_KEY, Config.OPENAI_API_VERSION]):
                raise ValueError(
                    "Azure OpenAI credentials are not properly configured. "
                    "Please check OPENAI_ENDPOINT, OPENAI_API_KEY, and OPENAI_API_VERSION."
                )

            try:
                AzureOpenAIClient._instance = AzureOpenAI(
                    azure_endpoint= Config.OPENAI_ENDPOINT,
                    api_key=Config.OPENAI_API_KEY,
                    api_version=Config.OPENAI_API_VERSION
                )
                logger.info("Azure OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Azure OpenAI client: {str(e)}")
                raise

        return AzureOpenAIClient._instance

    @staticmethod
    def get_chat_completion(
        messages: List[Dict[str, Any]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
        tools: Optional[List[Dict[str, Any]]] = None
    ):
        """Get chat completion from Azure OpenAI with improved error handling."""
        client = AzureOpenAIClient.get_instance()
        
        try:
            # Validate messages
            if not messages:
                raise ValueError("Messages list cannot be empty")
            
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
            
            logger.info(f"Making API request with {len(messages)} messages")
            response = client.chat.completions.create(**request_params)
            
            logger.info("Successfully received response from Azure OpenAI")
            return response
            
        except Exception as e:
            error_msg = f"Error in chat completion: {str(e)}"
            logger.error(error_msg)
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return None

class OnboardingAssistant:
    def __init__(self):
        """Initialize the OnboardingAssistant with enhanced functionality."""
        self.system_prompt = Prompt.SYSTEM_PROMPT
        self.conversation_history: List[Dict[str, Any]] = []
        self.chat_history_file = Config.CHAT_HISTORY_PATH

        # Enhanced function definitions with better descriptions
        self.function_definitions = [
        {
            "type": "function",
            "function": {
                "name": "get_member_information",
                "description": """Get team member information organized by projects.
                
                Data structure: projects[] -> members[] with fields like name, role, email, department, team, manager, hire_date, skills, status, phone, location
                
                Use for: team questions, contact info, roles, project assignments, "who works on X", "what's John's role", "team structure" """,
                "parameters": {"type": "object", "properties": {}, "required": []}
            }
        },
        {
            "type": "function", 
            "function": {
                "name": "get_process_information",
                "description": """Get company processes and workflows organized by projects.
                
                Data structure: projects[] -> processes[] with fields like process_name, description, status, dates, responsible_members, deliverables, dependencies, progress_percentage

                Use for: workflow questions, process status, timelines, responsibilities, "how do we do X", "what's the status of Y", "who handles Z" """,
                "parameters": {"type": "object", "properties": {}, "required": []}
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_techstack_information", 
                "description": """Get technology stack information organized by projects.
                
                Data structure: projects[] -> tech_stack{frontend, backend, database, ai_ml, cloud, tools} with fields like technology, version, purpose, status, documentation_url, support_team, learning_resources
                
                Use for: technology questions, tool info, versions, documentation, "what tech do we use", "which database", "where to learn React" """,
                "parameters": {"type": "object", "properties": {}, "required": []}
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_user_project_assignment",
                "description": """Get the current user's project assignment(s) based on their name and optional department.
                
                Data structure: user_found (boolean), total_projects (int), projects[] with fields like project_code, project_name, department, status, description, member_info (employee_id, name, role, email, team, manager, hire_date, status)
                
                Use for: finding user's project assignments, checking current projects, "what project am I assigned to", "which team am I in" """,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_name": {"type": "string", "description": "The name of the user to look up"},
                        "user_department": {"type": "string", "description": "Optional department filter"}
                    },
                    "required": ["user_name"]
                }
            }
        }
        ]
        # Function mapping for cleaner execution
        self.function_map = {
            "get_member_information": get_member_information,
            "get_process_information": get_process_information,
            "get_techstack_information": get_techstack_information,
            "get_user_project_assignment": get_user_project_assignment
        }
        
        self.reset_conversation()
        logger.info("OnboardingAssistant initialized successfully")

    def save_conversation_history(self, role: str, content: str):
        """Save conversation history to a file."""
        try:
            with open(self.chat_history_file, 'a', encoding='utf-8') as file:
                file.write(f"{role}: {content}\n")
            logger.info("Conversation history saved successfully")
        except Exception as e:
            logger.error(f"Error saving conversation history: {str(e)}")
            
    def clear_conversation_history(self):
        """Clear conversation history file."""
        try:
            with open(self.chat_history_file, 'w', encoding='utf-8') as file:
                file.write("")  # Clear the file
            logger.info("Conversation history cleared successfully")
        except Exception as e:
            logger.error(f"Error clearing conversation history: {str(e)}")

    def set_additional_context(self, context: str):
        """Set additional context for the conversation."""
        if not context:
            logger.warning("No context provided to set")
            return
        
        # Add context as a user message
        self.conversation_history.append({
            "role": "user",
            "content": context
        })
        logger.info(f"Additional context set: {context[:100]}...")

    def reset_conversation(self):
        """Reset conversation history to initial state."""
        self.conversation_history = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        self.conversation_history.extend(Prompt.FEW_SHOT_EXAMPLES)
        self.clear_conversation_history()
        logger.info("Conversation history reset")

    def _validate_input(self, user_message: str) -> bool:
        """Validate user input."""
        if not user_message or not user_message.strip():
            return False
        if len(user_message.strip()) > 10000:  # Reasonable limit
            logger.warning(f"Message too long: {len(user_message)} characters")
            return False
        return True

    def _handle_tool_calls(self, response) -> str:
        """Handle function calls from the AI response with improved error handling."""
        try:
            tool_calls = response.choices[0].message.tool_calls
            if not tool_calls:
                return "No tool calls found in response"
            
            # First, add the assistant message with tool calls to conversation history
            assistant_message = {
                "role": "assistant",
                "content": response.choices[0].message.content,
                "tool_calls": []
            }
            
            # Build the tool calls structure
            for tool_call in tool_calls:
                assistant_message["tool_calls"].append({
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                })
            
            # Add assistant message FIRST (this is crucial for the API)
            self.conversation_history.append(assistant_message)
            
            # Then execute functions and add tool responses
            results = []
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                
                # Execute the function
                if function_name in self.function_map:
                    try:
                        function_result = self.function_map[function_name]()
                        logger.info(f"Successfully executed function: {function_name}")
                        results.append(function_result)
                    except Exception as e:
                        error_msg = f"Error executing {function_name}: {str(e)}"
                        logger.error(error_msg)
                        results.append(error_msg)
                else:
                    error_msg = f"Unknown function call: {function_name}"
                    logger.error(error_msg)
                    results.append(error_msg)
                
                # Add tool response immediately after each function execution
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
            return error_msg

    def _get_final_response(self) -> str:
        """Get the final response from the AI after function execution."""
        try:
            follow_up_response = AzureOpenAIClient.get_chat_completion(
                self.conversation_history
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
                return "I've retrieved the information, but couldn't generate a proper response. Please try rephrasing your question."
                
        except Exception as e:
            error_msg = f"Error generating final response: {str(e)}"
            logger.error(error_msg)
            return "I encountered an error while processing the information. Please try again."

    def send_message(self, user_message: str) -> str:
        self.save_conversation_history("user", user_message)
        response = self.__send_message(user_message)
        self.save_conversation_history("assistant", response)
        return response

    def __send_message(self, user_message: str) -> str:
        """Send a message to the assistant and get a response."""
        try:
            # Validate input
            if not self._validate_input(user_message):
                return "Please provide a valid message (not empty and not too long)."
        
            # Add user message to conversation history
            self.conversation_history.append({
                "role": "user", 
                "content": user_message.strip()
            })
            logger.info(f"Processing user message: {user_message[:100]}...")
            
            # Get initial response from AI
            response = AzureOpenAIClient.get_chat_completion(
                self.conversation_history, 
                tools=self.function_definitions
            )
            
            if response is None:
                logger.error("No response from Azure OpenAI")
                # Remove the user message from history since we couldn't process it
                self.conversation_history.pop()
                return "I'm having trouble connecting to the AI service. Please try again in a moment."
            # Check if the response has tool calls (function calls)
            if (response.choices and 
                response.choices[0].message.tool_calls):
                
                logger.info("Processing function call(s)")
                self._handle_tool_calls(response)
                return self._get_final_response()
                
            else:
                # Regular response without function calls
                if (response.choices and 
                    response.choices[0].message.content):
                    
                    content = response.choices[0].message.content
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": content
                    })
                    logger.info("Regular response processed successfully")
                    return content
                else:
                    logger.warning("No content in response")
                    return "I didn't receive a proper response. Please try rephrasing your question."
                    
        except Exception as e:
            error_msg = f"Unexpected error in send_message: {str(e)}"
            logger.error(error_msg)
            logger.error(f"Full traceback: {traceback.format_exc()}")
            
            # Try to recover by removing the last user message
            if self.conversation_history and self.conversation_history[-1]["role"] == "user":
                self.conversation_history.pop()
            
            return "I encountered an unexpected error. Please try again with a different question."

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get a copy of the current conversation history."""
        return [msg.copy() for msg in self.conversation_history]
    
    def get_conversation_length(self) -> int:
        """Get the number of messages in conversation history."""
        return len(self.conversation_history)
    
    def clear_conversation_except_system(self):
        """Clear conversation history but keep the system prompt."""
        system_message = self.conversation_history[0] if self.conversation_history else None
        self.conversation_history = [system_message] if system_message else []
        logger.info("Conversation cleared except system message")
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the current conversation."""
        user_messages = [msg for msg in self.conversation_history if msg["role"] == "user"]
        assistant_messages = [msg for msg in self.conversation_history if msg["role"] == "assistant"]
        tool_messages = [msg for msg in self.conversation_history if msg["role"] == "tool"]
        
        return {
            "total_messages": len(self.conversation_history),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "tool_calls": len(tool_messages),
            "conversation_started": len(self.conversation_history) > 1
        }

def main():
    """Main function to run the interactive chat."""
    try:
        assistant = OnboardingAssistant()
        print("🤖 Welcome to the Employee Onboarding Assistant!")
        print("I can help you with information about team members, processes, and our tech stack.")
        print("Type 'exit', 'quit', or 'bye' to end the conversation.")
        print("Type 'reset' to start a new conversation.")
        print("Type 'history' to see conversation summary.")
        print("-" * 60)
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("\n👋 Thank you for using the Onboarding Assistant. Goodbye!")
                    break
                elif user_input.lower() == "reset":
                    assistant.reset_conversation()
                    print("\n🔄 Conversation reset. How can I help you?")
                    continue
                elif user_input.lower() == "history":
                    summary = assistant.get_conversation_summary()
                    print(f"\n📊 Conversation Summary:")
                    print(f"   Total messages: {summary['total_messages']}")
                    print(f"   Your messages: {summary['user_messages']}")
                    print(f"   My responses: {summary['assistant_messages']}")
                    print(f"   Information lookups: {summary['tool_calls']}")
                    continue
                elif not user_input:
                    print("Please enter a message or type 'exit' to quit.")
                    continue
                
                print("\n🤔 Thinking...")
                response = assistant.send_message(user_input)
                print(f"\n🤖 Assistant: {response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except EOFError:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                print(f"\n❌ An unexpected error occurred: {str(e)}")
                print("Please try again or type 'exit' to quit.")
    
    except Exception as e:
        logger.error(f"Fatal error in main: {str(e)}")
        print(f"❌ Failed to start the assistant: {str(e)}")
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    main()