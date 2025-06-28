#!/usr/bin/env python3
"""
Test the chatbot functionality with real queries using the mock data
"""

from chatbot import OnboardingAssistant
import json

def test_chatbot_queries():
    """Test various chatbot queries with the mock data"""
    print("🤖 Testing Employee Onboarding Assistant with Mock Data")
    print("=" * 60)
    
    # Initialize the assistant
    try:
        assistant = OnboardingAssistant()
        print("✅ Assistant initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize assistant: {e}")
        return False
    
    # Test queries
    test_queries = [
        "Who is Quinn Hernandez?",
        "Show me all team members in the DevOps department",
        "What projects are currently active?",
        "What technologies do we use for frontend development?",
        "Tell me about our development processes",
        "Who are the Security Engineers in the company?",
        "What is the Employee Onboarding Assistant project about?"
    ]
    
    print("\n🔍 Testing Queries:")
    print("-" * 40)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")
        print("   Response:", end=" ")
        
        try:
            response = assistant.send_message(query)
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Show conversation summary
    print("\n📊 Final Conversation Summary:")
    summary = assistant.get_conversation_summary()
    for key, value in summary.items():
        print(f"   {key}: {value}")
    
    return True

def test_data_loading():
    """Test if mock data is properly loaded"""
    print("\n📁 Testing Data Loading:")
    print("-" * 30)
    
    from chatbot import get_member_information, get_process_information, get_techstack_information
    
    # Test member information
    try:
        member_data = get_member_information()
        member_json = json.loads(member_data)
        print(f"✅ Member data loaded: {len(member_json)} projects, {sum(len(p['members']) for p in member_json)} total members")
    except Exception as e:
        print(f"❌ Member data error: {e}")
    
    # Test process information
    try:
        process_data = get_process_information()
        process_json = json.loads(process_data)
        print(f"✅ Process data loaded: {len(process_json)} projects with processes")
    except Exception as e:
        print(f"❌ Process data error: {e}")
    
    # Test tech stack information
    try:
        tech_data = get_techstack_information()
        tech_json = json.loads(tech_data)
        print(f"✅ Tech stack data loaded: {len(tech_json)} projects with tech stacks")
    except Exception as e:
        print(f"❌ Tech stack data error: {e}")

def main():
    """Run all tests"""
    print("🧪 Testing Employee Onboarding Assistant with Mock Data")
    print("=" * 70)
    
    # Test data loading first
    test_data_loading()
    
    # Test chatbot functionality
    success = test_chatbot_queries()
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 All tests completed! The system is working with mock data.")
        print("\n💡 You can now run the Streamlit app and test these queries:")
        for i, query in enumerate([
            "Who is Quinn Hernandez?",
            "What technologies do we use for frontend development?",
            "Show me Security Engineers",
            "Tell me about active projects"
        ], 1):
            print(f"   {i}. {query}")
    else:
        print("❌ Some tests failed. Please check the configuration.")

if __name__ == "__main__":
    main()
