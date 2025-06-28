# Employee Onboarding Chatbot

A Streamlit-based chatbot application for employee onboarding that integrates with Azure OpenAI to provide intelligent responses about company information, team members, processes, and technology stack.

## Features

- 🤖 **AI-Powered Chatbot**: Uses Azure OpenAI for intelligent responses
- 👥 **Team Information**: Get details about team members, roles, and contacts
- 📋 **Process Information**: Learn about company processes and workflows
- 🛠️ **Tech Stack Info**: Discover technology tools and frameworks used
- 💬 **Interactive Chat**: Modern Streamlit-based chat interface
- 🔄 **Conversation Management**: Reset conversations and view summaries
- 📊 **Chat Statistics**: Track conversation metrics

## Files Structure

```
myEOC/
├── app.py                 # Streamlit web application
├── chatbot.py            # Core chatbot logic and Azure OpenAI integration
├── config.py             # Configuration settings
├── prompt.py             # System prompts and few-shot examples
├── session_manager.py    # Session management (if needed)
├── requirements.txt      # Python dependencies
├── start_app.py         # Startup script
├── test_integration.py  # Integration tests
└── data/                # Data files
    ├── member_info.json     # Team member information
    ├── processes.json       # Company processes
    ├── techstack.json       # Technology stack information
    └── chat_history.json    # Chat history storage
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Azure OpenAI

Edit `config.py` to set up your Azure OpenAI credentials:

```python
# Azure OpenAI Configuration
OPENAI_ENDPOINT = "your-azure-openai-endpoint"
OPENAI_API_KEY = "your-api-key"
OPENAI_API_VERSION = "2024-02-15-preview"
OPENAI_DEPLOYMENT_NAME = "your-deployment-name"
```

### 3. Prepare Data Files

Ensure the following JSON files exist in the `data/` directory:
- `member_info.json`: Team member information
- `processes.json`: Company processes and procedures
- `techstack.json`: Technology stack details

### 4. Test the Setup

Run the integration test to verify everything is working:

```bash
python test_integration.py
```

### 5. Start the Application

#### Option 1: Using the startup script
```bash
python start_app.py
```

#### Option 2: Direct Streamlit command
```bash
streamlit run app.py
```

## Usage

1. **Welcome Screen**: Enter your full name to start
2. **Chat Interface**: Ask questions about:
   - Team members and contacts
   - Company processes and policies
   - Technology stack and tools
   - General onboarding information

3. **Sidebar Features**:
   - Reset conversation
   - View conversation summary
   - Start over with new name

## Example Questions

- "Who is the team lead for the backend development team?"
- "What is our vacation policy?"
- "What programming languages do we use for web development?"
- "How do I set up my development environment?"
- "Who should I contact for IT support?"

## Architecture

### Core Components

1. **OnboardingAssistant Class** (`chatbot.py`):
   - Manages conversation history
   - Handles Azure OpenAI API calls
   - Executes function calls for data retrieval
   - Provides error handling and logging

2. **Streamlit Interface** (`app.py`):
   - User-friendly chat interface
   - Session state management
   - Real-time conversation display
   - Interactive controls

3. **Data Functions**:
   - `get_member_information()`: Retrieves team member data
   - `get_process_information()`: Retrieves process information
   - `get_techstack_information()`: Retrieves tech stack data

### Function Calling

The chatbot uses Azure OpenAI's function calling feature to:
1. Determine when to retrieve specific information
2. Call appropriate data functions
3. Process and format responses
4. Provide contextual answers

## Configuration

Key configuration options in `config.py`:
- Azure OpenAI credentials
- File paths for data sources
- Logging settings
- API parameters

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration Errors**: Check Azure OpenAI settings in `config.py`

3. **Data File Errors**: Verify JSON files exist and are properly formatted

4. **API Errors**: Check Azure OpenAI endpoint and API key

### Logs

The application logs important events and errors. Check the console output for debugging information.

## Development

### Running Tests

```bash
python test_integration.py
```

### Adding New Features

1. **New Data Sources**: Add new JSON files and corresponding functions
2. **New Function Calls**: Update `function_definitions` in `OnboardingAssistant`
3. **UI Improvements**: Modify `app.py` for interface changes

## Security Notes

- Keep Azure OpenAI credentials secure
- Don't commit sensitive information to version control
- Use environment variables for production deployments
- Validate user inputs to prevent security issues

## Support

For issues or questions:
1. Check the logs for error messages
2. Run the integration test to verify setup
3. Review configuration settings
4. Ensure all data files are present and valid

---

**Built with**: Python, Streamlit, Azure OpenAI, and JSON data storage
