import streamlit as st
from datetime import datetime
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Page Config ---
st.set_page_config(
    page_title="📱 Smartphone Consultant AI", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Initialize Session State ---
def initialize_session_state():
    """Initialize all session state variables"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "conversation_count" not in st.session_state:
        st.session_state.conversation_count = 0

# --- Modern Minimalist CSS ---
def apply_modern_minimalist_css():
    """Apply modern minimalist CSS based on current theme"""
    theme_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
        color: #e8e8e8;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .block-container {
        padding: 1rem;
        max-width: 900px;
    }
    
    /* Main chat container */
    .chat-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    /* Header styling */
    .chat-header {
        text-align: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .chat-header h1 {
        font-size: 2.25rem;
        font-weight: 600;
        color: #ffffff;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.025em;
    }
    
    .chat-header p {
        font-size: 1.1rem;
        color: #a0a0a0;
        margin: 0;
        font-weight: 400;
    }
    
    /* Sidebar styling */
    .sidebar .stButton > button {
        width: 100%;
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 0.75rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .sidebar .stButton > button:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.3);
        transform: translateY(-1px);
    }
    
    .sidebar h3 {
        color: #ffffff;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }
    
    .sidebar .stMarkdown p, .sidebar .stMarkdown li {
        color: #b0b0b0;
        font-size: 0.9rem;
    }
    
    /* Message styling */
    .stChatMessage {
        margin: 1rem 0;
        border-radius: 20px;
        border: none;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .stChatMessage[data-testid="chat-message-user"] {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        margin-left: 15%;
    }
    
    .stChatMessage[data-testid="chat-message-assistant"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-right: 15%;
    }
    
    /* Chat input area - integrated into conversation */
    .stChatInput {
        margin: 1rem 0 0.5rem 0;
        padding: 0;
    }
    
    .stChatInput > div {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        backdrop-filter: blur(10px);
        margin: 0;
    }
    
    .stChatInput input {
        background: transparent;
        color: #ffffff;
        border: none;
        font-size: 1rem;
        padding: 1rem 1.5rem;
    }
    
    .stChatInput input::placeholder {
        color: #888888;
    }
    
    /* Button styling */
    .stButton > button {
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.3);
        transform: translateY(-1px);
    }
    
    /* Welcome message */
    .welcome-assistant {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    /* Timestamps */
    .stChatMessage small {
        color: #888888;
        font-size: 0.875rem;
    }
    </style>
    """
    st.markdown(theme_css, unsafe_allow_html=True)

# --- LLM Integration Point ---
def get_ai_response(user_message: str) -> str:
    """
    This is where you'll integrate your LLM
    Replace this placeholder with your actual LLM integration
    """
    # TODO: Replace this with your LLM integration
    
    # Placeholder response logic (remove when integrating your LLM)
    user_message_lower = user_message.lower()
    
    # Simple keyword-based responses for demonstration
    if any(word in user_message_lower for word in ["iphone", "apple"]):
        return "🍎 I'd be happy to help you with iPhone recommendations! The latest iPhone 15 series offers excellent camera quality and performance. What specific features are most important to you - camera, battery life, or something else?"
    
    elif any(word in user_message_lower for word in ["android", "samsung", "google"]):
        return "🤖 Great choice looking at Android options! Samsung Galaxy and Google Pixel phones offer excellent value. What's your budget range and primary use case? This will help me recommend the perfect Android device for you."
    
    elif any(word in user_message_lower for word in ["budget", "cheap", "affordable"]):
        return "💰 I can definitely help you find great value smartphones! For budget-friendly options, I'd recommend looking at phones like the Google Pixel 7a, Samsung Galaxy A54, or OnePlus Nord series. What's your specific budget range?"
    
    elif any(word in user_message_lower for word in ["camera", "photography", "photo"]):
        return "📸 For photography enthusiasts, I'd recommend phones with excellent camera systems like the iPhone 15 Pro, Google Pixel 8 Pro, or Samsung Galaxy S24 Ultra. Each excels in different areas - which type of photography do you do most?"
    
    elif any(word in user_message_lower for word in ["gaming", "performance"]):
        return "🎮 For gaming, you'll want a phone with a powerful processor and good cooling. The iPhone 15 Pro Max, Samsung Galaxy S24 Ultra, and ASUS ROG Phone series are excellent choices. What games do you play most?"
    
    elif any(word in user_message_lower for word in ["battery", "charging"]):
        return "🔋 Battery life is crucial! Phones like the iPhone 15 Plus, Samsung Galaxy S24+, and OnePlus 12 offer excellent battery performance. Do you prefer fast charging or longer overall battery life?"
    
    else:
        return f"I understand you're asking about: '{user_message}'. As your smartphone consultant, I'm here to help you find the perfect device! Could you provide more details about your specific needs, budget, or preferences so I can give you the best recommendation?"

# --- Sidebar ---
def create_sidebar():
    """Create the left sidebar with theme toggle and controls"""
    with st.sidebar:
        st.markdown("### ⚙️ Controls")
        st.markdown("---")
        
        # Chat statistics
        if st.session_state.chat_history:
            st.markdown("### 📊 Chat Stats")
            total_messages = len(st.session_state.chat_history)
            user_messages = len([m for m in st.session_state.chat_history if m["role"] == "user"])
            assistant_messages = total_messages - user_messages
            
            st.markdown(f"""
            - **Total messages:** {total_messages}
            - **Your questions:** {user_messages}  
            - **AI responses:** {assistant_messages}
            """)
            
            st.markdown("---")
        
        # About section
        st.markdown("### ℹ️ About")
        st.markdown("This is your AI-powered smartphone consultant. Ask me anything about phones, comparisons, recommendations, or tech specifications.")
        
        st.markdown("---")
        st.markdown("### 💡 Quick Tips")
        st.markdown("""
        - Be specific about your needs
        - Mention your budget range  
        - Ask for comparisons
        - Inquire about specific features
        """)
        
        # Status indicator
        st.markdown("---")
        st.markdown("🟢 **AI Online & Ready**")

# --- Chat Interface ---
def handle_user_input(user_input: str):
    """Handle user input and generate AI response"""
    if not user_input or len(user_input.strip()) == 0:
        return
    
    # Add user message to chat history
    st.session_state.chat_history.append({
        "role": "user", 
        "content": user_input,
        "timestamp": datetime.now()
    })
    
    # Get AI response
    with st.spinner("Thinking..."):
        try:
            # Simulate processing time
            time.sleep(1)
            
            # Get AI response - replace this with your LLM integration
            ai_response = get_ai_response(user_input)
            
            # Add AI response to chat history
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": ai_response,
                "timestamp": datetime.now()
            })
            
            st.session_state.conversation_count += 1
            
        except Exception as e:
            error_message = "I apologize, but I'm experiencing some technical difficulties. Please try asking your question again."
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": error_message,
                "timestamp": datetime.now()
            })
            logger.error(f"Error generating AI response: {str(e)}")

def display_chat_interface():
    """Display the main chat interface"""
    # Header inside the container
    st.markdown("""
        <div class="chat-header">
            <h1>📱 Smartphone Consultant</h1>
            <p>Your AI assistant for finding the perfect smartphone</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Display welcome message if no chat history
    if not st.session_state.chat_history:
        st.markdown("""
            <div class="welcome-assistant">
                <p style="margin: 0; font-size: 1.1rem; color: inherit;">
                    🤖 Hi! I'm your AI Smartphone Consultant. I can help you find the perfect phone, 
                    compare devices, or answer any smartphone-related questions. What would you like to know?
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Display chat history with modern icons
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user", avatar="👨‍💻"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(message["content"])
                
                # Add timestamp for assistant messages
                timestamp = message.get("timestamp", datetime.now())
                st.caption(f"*{timestamp.strftime('%H:%M')}*")
    
    # Chat input within the conversation area
    user_input = st.chat_input(
        "Ask me anything about smartphones...",
        key="chat_input"
    )
    
    if user_input:
        # Validate input
        if len(user_input) > 1000:
            st.warning("Please keep your question under 1000 characters.")
            return
        
        # Display user message immediately
        with st.chat_message("user", avatar="👨‍💻"):
            st.markdown(user_input)
        
        # Handle the input and get response
        handle_user_input(user_input)
        
        # Rerun to update the chat display
        st.rerun()
    
    # Clear chat button
    if st.session_state.chat_history:
        st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.conversation_count = 0
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Main Application ---
def main():
    """Main application logic"""
    initialize_session_state()
    
    # Apply modern minimalist CSS
    apply_modern_minimalist_css()
    
    # Create sidebar
    create_sidebar()
    
    # Display chat interface
    display_chat_interface()

if __name__ == "__main__":
    main()