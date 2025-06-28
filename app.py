import streamlit as st
from datetime import datetime
from chatbot import OnboardingAssistant
import logging

# Configure logging for the Streamlit app
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Page Config ---
st.set_page_config(page_title="🧑‍💼 Onboarding Assistant", layout="centered")

# --- Custom Style ---
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stChatMessage {
        padding: 12px;
        border-radius: 12px;
        margin: 8px 0;
    }
    .stChatMessage.user {
        background: linear-gradient(to right, #d9fdd3, #baf1c9);
        align-self: flex-end;
        text-align: right;
    }
    .stChatMessage.assistant {
        background: linear-gradient(to right, #f1f1f1, #e0e0e0);
        align-self: flex-start;
    }
    .chat-box {
        border: 1px solid #ccc;
        border-radius: 16px;
        padding: 20px;
        max-height: 600px;
        overflow-y: auto;
        background: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- Ask Full Name ---
if "user_name" not in st.session_state:
    with st.form("name_form"):
        st.title("🧑‍💼 Welcome to Employee Onboarding Chatbot")
        st.markdown("Let's get started. What's your full name?")
        full_name = st.text_input("Full Name")
        submitted = st.form_submit_button("Start Chat")

        if submitted and full_name:
            st.session_state.user_name = full_name.strip().split()[
                0]   # First name
            st.session_state.chat = [
                {"role": "assistant", "content": f"Hi {st.session_state.user_name} 👋 I'm here to help you get started at the company!"}
            ]
            st.rerun()


# --- Main Chat UI ---
elif "user_name" in st.session_state:

    # Sidebar with additional options
    with st.sidebar:
        st.title("🛠️ Chat Options")
        
        if st.button("🔄 Reset Conversation"):
            if "assistant" in st.session_state:
                st.session_state.assistant.reset_conversation()
            st.session_state.chat = [
                {"role": "assistant", "content": f"Hi {st.session_state.user_name} 👋 I'm here to help you get started at the company!"}
            ]
            st.rerun()
        
        if st.button("📊 Show Conversation Summary"):
            if "assistant" in st.session_state:
                summary = st.session_state.assistant.get_conversation_summary()
                st.write("**Conversation Statistics:**")
                st.write(f"- Total messages: {summary['total_messages']}")
                st.write(f"- Your messages: {summary['user_messages']}")
                st.write(f"- Assistant responses: {summary['assistant_messages']}")
                st.write(f"- Information lookups: {summary['tool_calls']}")
        
        if st.button("👋 Start Over"):
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.title(f"💬 Hello {st.session_state.user_name}!")
    st.markdown(
        "Ask anything about your onboarding process, benefits, documents, and more.")
    with st.expander("💡 Things I can help you with (click to expand)", expanded=False):
        st.markdown("""
        - ✅ **Company Policies & Processes** - Ask about leave policy, remote work, probation period, dress code, workflows, and procedures.
        - 👥 **Team & People** - Find out who is in your team, contact information, roles, and project assignments.
        - 🛠️ **Technology Stack** - Learn about development tools, frameworks, programming languages, and technical resources.
        - 🎯 **Company Information** - Discover our mission, values, events, and organizational structure.
        - 💻 **Getting Started** - Get help with onboarding processes and initial setup.
        
        **Pro tip:** Be specific in your questions for better answers! For example:
        - "Who is the team lead for the backend development team?"
        - "What is our vacation policy?"
        - "What programming languages do we use for web development?"
        """)

    # Chat history init
    if "chat" not in st.session_state:
        st.session_state.chat = [
            {"role": "assistant", "content": f"Hi {st.session_state.user_name} 👋 I'm here to help you get started at the company!"}
        ]
    
    # Initialize the OnboardingAssistant if not already done
    if "assistant" not in st.session_state:
        with st.spinner("🔧 Initializing assistant..."):
            try:
                st.session_state.assistant = OnboardingAssistant()
                logger.info("OnboardingAssistant initialized successfully")
                st.success("✅ Assistant ready!")
            except Exception as e:
                st.error(f"❌ Failed to initialize the assistant: {str(e)}")
                st.error("Please check your configuration (config.py) and ensure all required files are in place.")
                st.stop()
    
    # Show assistant status in sidebar
    with st.sidebar:
        if "assistant" in st.session_state:
            st.success("✅ Assistant Connected")
        else:
            st.error("❌ Assistant Not Available")

    # Display chat history
    chat_container = st.container()
    with chat_container:
        for i, msg in enumerate(st.session_state.chat):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
                # Add timestamp for assistant messages (except the first welcome message)
                if msg["role"] == "assistant" and i > 0:
                    st.caption(f"*{datetime.now().strftime('%H:%M')}*")

    # Chat input
    prompt = st.chat_input(
        f"What would you like to know, {st.session_state.user_name}?")

    if prompt:
        # Validate input
        prompt = prompt.strip()
        if not prompt:
            st.warning("Please enter a valid message.")
            st.stop()
        
        if len(prompt) > 1000:
            st.warning("Message is too long. Please keep it under 1000 characters.")
            st.stop()
        
        # Add user message to chat history
        st.session_state.chat.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process and display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            with st.spinner("🤔 Thinking..."):
                try:
                    # Get response from the OnboardingAssistant
                    response = st.session_state.assistant.send_message(prompt)
                    
                    # Display the response
                    message_placeholder.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.chat.append({
                        "role": "assistant",
                        "content": response
                    })
                    
                except Exception as e:
                    error_message = "I'm sorry, I encountered an error while processing your request. Please try again or contact support if the issue persists."
                    message_placeholder.error(error_message)
                    logger.error(f"Error processing message: {str(e)}")
                    
                    # Add error response to chat history
                    st.session_state.chat.append({
                        "role": "assistant",
                        "content": f"❌ {error_message}"
                    })
        
        # Auto-rerun to update the chat display
        st.rerun()
