#!/usr/bin/env python3
"""
Enhanced test suite for the Employee Onboarding Assistant
Based on the existing test approach but with improved coverage and error handling
"""

from chatbot import OnboardingAssistant
import json
import time

def test_onboarding_scenarios():
    """Test  onboarding scenarios with better validation"""
    print("🤖 Testing Enhanced Employee Onboarding Assistant")
    print("=" * 70)
    
    # Initialize the assistant
    try:
        assistant = OnboardingAssistant()
        print("✅ Assistant initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize assistant: {e}")
        return False
    
    # Enhanced test scenarios covering real onboarding use cases
    test_scenarios = [
        {
            "category": "👥 Team Information",
            "queries": [
                "Who is Quinn Hernandez?",
                "Show me all team members in the DevOps department",
                "Who are the Security Engineers in the company?",
                "List all members in the Engineering department",
                "Find information about Sarah Johnson"
            ]
        },
        {
            "category": "📋 Project Information", 
            "queries": [
                "What projects are currently active?",
                "What is the Employee Onboarding Assistant project about?",
                "Tell me about project AIAE001",
                "Which projects are in the Engineering department?",
                "What's the status of the Customer Portal project?"
            ]
        },
        {
            "category": "💻 Technology Stack",
            "queries": [
                "What technologies do we use for frontend development?",
                "What database technologies do we use?",
                "What AI/ML tools are available in our projects?",
                "Tell me about our backend technology stack",
                "What cloud platforms do we use?"
            ]
        },
        {
            "category": "⚙️ Development Processes",
            "queries": [
                "Tell me about our development processes",
                "What is our code review process?",
                "How do we handle sprint planning?",
                "What's our deployment process?",
                "Tell me about our testing procedures"
            ]
        },
        {
            "category": "🔍 Personal Assignment",
            "queries": [
                "What project am I assigned to?",
                "Who is my manager?",
                "What team will I be working with?",
                "What's my role in the project?",
                "When did I start working here?"
            ]
        },
        {
            "category": "🌟 Natural Language Queries",
            "queries": [
                "I'm new here, can you help me understand our team structure?",
                "Where can I find documentation for our technology stack?",
                "Who should I contact about project assignments?",
                "I need to learn about our development workflow",
                "Help me understand what tools I'll be using"
            ]
        },
        {
            "category": "⚠️ Error Handling & Edge Cases",
            "queries": [
                "Find information about John Doe",  # Non-existent user
                "What's the tech stack for project XYZ?",  # Non-existent project
                "",  # Empty query
                "a" * 100,  # Very long query
                "Tell me about department ABC"  # Non-existent department
            ]
        },
        {
            "category": "🚫 Out-of-Scope Queries",
            "queries": [
                "What's my salary?",
                "How do I book vacation time?",
                "My laptop is broken, who do I contact?",
                "What are the office hours?",
                "How do I submit an expense report?"
            ]
        }
    ]
    
    total_queries = 0
    successful_responses = 0
    errors = 0
    out_of_scope_handled = 0
    
    print("\n🔍 Testing  Onboarding Scenarios:")
    print("-" * 50)
    
    for scenario in test_scenarios:
        print(f"\n{scenario['category']}")
        print("─" * len(scenario['category']))
        
        for i, query in enumerate(scenario['queries'], 1):
            total_queries += 1
            print(f"\n{i}. Query: {query}")
            
            if not query.strip():
                print("   ⚠️  Skipping empty query")
                continue
                
            print("   Processing...", end=" ")
            
            try:
                start_time = time.time()
                response = assistant.send_message(query)
                response_time = time.time() - start_time
                
                # Validate response quality
                if not response:
                    print("❌ Empty response")
                    errors += 1
                elif len(response) < 10:
                    print("⚠️  Very short response")
                    print(f"   Response: {response}")
                elif "error" in response.lower() and "system error" in response.lower():
                    print("❌ System error detected")
                    errors += 1
                elif any(keyword in response.lower() for keyword in ["contact hr", "contact it", "out of scope"]):
                    print("✅ Out-of-scope handled correctly")
                    out_of_scope_handled += 1
                    successful_responses += 1
                else:
                    print("✅ Good response")
                    successful_responses += 1
                
                print(f"   Time: {response_time:.2f}s")
                print(f"   Length: {len(response)} chars")
                
                # Show first 100 characters of response
                preview = response.replace('\n', ' ')[:100]
                print(f"   Preview: {preview}...")
                
            except Exception as e:
                print(f"❌ Exception: {e}")
                errors += 1
    
    # Performance and conversation summary
    print(f"\n📊 Test Results Summary:")
    print("─" * 30)
    summary = assistant.get_conversation_summary()
    
    print(f"Total queries tested: {total_queries}")
    print(f"Successful responses: {successful_responses}")
    print(f"Errors encountered: {errors}")
    print(f"Out-of-scope handled: {out_of_scope_handled}")
    print(f"Success rate: {(successful_responses/total_queries*100):.1f}%")
    
    print(f"\nConversation Statistics:")
    print(f"Total messages: {summary['total_messages']}")
    print(f"User messages: {summary['user_messages']}")
    print(f"Assistant responses: {summary['assistant_messages']}")
    print(f"Information lookups: {summary['tool_calls']}")
    
    return successful_responses > total_queries * 0.8  # 80% success rate

def test_data_loading():
    """Enhanced test for data loading with better error detection"""
    print("\n📁 Testing  Data Loading:")
    print("-" * 40)
    
    from chatbot import get_member_information, get_process_information, get_techstack_information, get_user_project_assignment
    
    test_results = {}
    
    # Test member information
    try:
        print("Testing member information loading...", end=" ")
        member_data = get_member_information()
        
        if "error" in member_data.lower():
            print("⚠️  Error detected in member data")
            test_results["member_info"] = "error"
        else:
            member_json = json.loads(member_data)
            total_members = sum(len(p.get('members', [])) for p in member_json)
            print(f"✅ Loaded: {len(member_json)} projects, {total_members} members")
            test_results["member_info"] = "success"
            
    except Exception as e:
        print(f"❌ Failed: {e}")
        test_results["member_info"] = "failed"
    
    # Test process information
    try:
        print("Testing process information loading...", end=" ")
        process_data = get_process_information()
        
        if "error" in process_data.lower():
            print("⚠️  Error detected in process data")
            test_results["process_info"] = "error"
        else:
            process_json = json.loads(process_data)
            total_processes = sum(len(p.get('processes', [])) for p in process_json)
            print(f"✅ Loaded: {len(process_json)} projects, {total_processes} processes")
            test_results["process_info"] = "success"
            
    except Exception as e:
        print(f"❌ Failed: {e}")
        test_results["process_info"] = "failed"
    
    # Test tech stack information
    try:
        print("Testing tech stack information loading...", end=" ")
        tech_data = get_techstack_information()
        
        if "error" in tech_data.lower():
            print("⚠️  Error detected in tech stack data")
            test_results["tech_info"] = "error"
        else:
            tech_json = json.loads(tech_data)
            print(f"✅ Loaded: {len(tech_json)} projects with tech stacks")
            test_results["tech_info"] = "success"
            
    except Exception as e:
        print(f"❌ Failed: {e}")
        test_results["tech_info"] = "failed"
    
    # Test user project assignment with different scenarios
    test_users = [
        ("Quinn Hernandez", "Known user"),
        ("John Smith", "Common name"),
        ("Sarah", "First name only"),
        ("NonExistent User", "Invalid user"),
        ("", "Empty name")
    ]
    
    print("\nTesting user project assignment lookup:")
    assignment_results = []
    
    for user_name, description in test_users:
        if not user_name:
            continue
            
        try:
            print(f"  Testing {description} ({user_name})...", end=" ")
            result = get_user_project_assignment(user_name)
            result_json = json.loads(result)
            
            if result_json.get("user_found"):
                projects = result_json.get("total_projects", 0)
                print(f"✅ Found {projects} project(s)")
                assignment_results.append("found")
            else:
                print("✅ Not found (handled correctly)")
                assignment_results.append("not_found")
                
        except Exception as e:
            print(f"❌ Failed: {e}")
            assignment_results.append("failed")
    
    # Summary
    print(f"\n📊 Data Loading Test Results:")
    for test_name, result in test_results.items():
        status_icon = "✅" if result == "success" else "⚠️" if result == "error" else "❌"
        print(f"  {status_icon} {test_name}: {result}")
    
    successful_tests = sum(1 for result in test_results.values() if result == "success")
    total_tests = len(test_results)
    
    return successful_tests == total_tests

def test_assistant_robustness():
    """Test assistant robustness and error recovery"""
    print("\n🛡️  Testing Assistant Robustness:")
    print("-" * 35)
    
    try:
        assistant = OnboardingAssistant()
        
        # Test conversation reset
        print("Testing conversation reset...", end=" ")
        initial_length = assistant.get_conversation_length()
        assistant.reset_conversation()
        reset_length = assistant.get_conversation_length()
        
        if reset_length > 0:
            print("✅ Reset successful")
        else:
            print("❌ Reset failed")
            
        # Test conversation management
        print("Testing conversation management...", end=" ")
        assistant.set_additional_context("I work in Engineering department")
        
        summary = assistant.get_conversation_summary()
        if summary.get("total_messages", 0) > 0:
            print("✅ Context management working")
        else:
            print("❌ Context management failed")
            
        return True
        
    except Exception as e:
        print(f"❌ Robustness test failed: {e}")
        return False

def main():
    """Run all enhanced tests"""
    print("🧪 Enhanced Employee Onboarding Assistant Test Suite")
    print("=" * 80)
    
    test_results = {}
    
    # Run data loading tests
    test_results["data_loading"] = test_data_loading()

    # Run robustness tests
    test_results["robustness"] = test_assistant_robustness()
    
    # Run  scenario tests
    test_results["scenarios"] = test_onboarding_scenarios()
    
    # Final summary
    print("\n" + "=" * 80)
    print("🎯 Final Test Results:")
    print("-" * 25)
    
    for test_name, result in test_results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {status}: {test_name.replace('_', ' ').title()}")
    
    all_passed = all(test_results.values())
    
    if all_passed:
        print("\n🎉 All tests passed! The system is working well.")
        print("\n💡 Recommended next steps:")
        print("   1. Test with the Streamlit app using these queries")
        print("   2. Validate responses with domain experts")
        print("   3. Test with real Azure OpenAI API integration")
        print("   4. Conduct user acceptance testing")
        print("   5. Monitor performance in production")
    else:
        print("\n⚠️  Some tests failed. Please review the issues above.")
        print("   Check your data files and configuration.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
