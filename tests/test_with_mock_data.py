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
        assistant.set_additional_context("My name is Nam Vu Son, My department is Engineering, and I am assigned to the Employee Onboarding Assistant project.")
        print("✅ Assistant initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize assistant: {e}")
        return False
    
    # Enhanced test queries covering  onboarding scenarios
    test_queries = [
        # Basic team information queries
        "Who is Drew Ramirez?",
        "Show me all team members in the DevOps department",
        "Who are the Security Engineers in the company?",
        
        # Project and assignment queries
        "What projects are currently active?",
        "What is the Employee Onboarding Assistant project about?",
        "What project am I assigned to?",
        
        # Technology stack queries
        "What technologies do we use for frontend development?",
        "What database technologies do we use?",
        "What AI/ML tools are available in our projects?",
        
        # Process and workflow queries
        "Tell me about our development processes",
        "What is our code review process?",
        "How do we handle sprint planning?",
        
        # Edge cases and error handling
        "Find information about John Doe",  # Non-existent user
        "What's the tech stack for project XYZ?",  # Non-existent project
        
        # Natural language variations
        "I'm new here, can you help me understand our team structure?",
        "Where can I find documentation for our technology stack?",
        "Who should I contact about project assignments?",
        
        # Out-of-scope queries (should be handled gracefully)
        "What's my salary?",
        "How do I book vacation time?",
        "My laptop is broken, who do I contact?",
        
        # Complex multi-part queries
        "Who is my manager and what project will I be working on?",
        "What technologies should I learn for my role and who can help me?",
        "Tell me about the team I'll be joining and our development process"
    ]
    
    print("\n🔍 Testing Queries:")
    print("-" * 40)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")
        print("   Response:", end=" ")
        
        try:
            response = assistant.send_message(query)
            print(f"✅ Response: {response[:100]}...")
            
            # Basic validation of response
            if len(response) < 10:
                print("⚠️  Warning: Very short response")
            elif "error" in response.lower():
                print("⚠️  Warning: Error detected in response")
            else:
                print("✅ Response looks good")
                
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
