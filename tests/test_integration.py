#!/usr/bin/env python3
"""
Test script to verify the integration between chatbot.py and app.py
"""

import sys
import os

def test_imports():
    """Test if all required imports work correctly"""
    print("Testing imports...")
    
    try:
        from chatbot import OnboardingAssistant
        print("✅ OnboardingAssistant import successful")
    except ImportError as e:
        print(f"❌ Failed to import OnboardingAssistant: {e}")
        return False
    
    try:
        import streamlit as st
        print("✅ Streamlit import successful")
    except ImportError as e:
        print(f"❌ Failed to import Streamlit: {e}")
        return False
    
    try:
        from config import Config
        print("✅ Config import successful")
    except ImportError as e:
        print(f"❌ Failed to import Config: {e}")
        return False
        
    try:
        from prompt import Prompt
        print("✅ Prompt import successful")
    except ImportError as e:
        print(f"❌ Failed to import Prompt: {e}")
        return False
    
    return True

def test_assistant_creation():
    """Test if OnboardingAssistant can be created"""
    print("\nTesting OnboardingAssistant creation...")
    
    try:
        from chatbot import OnboardingAssistant
        assistant = OnboardingAssistant()
        print("✅ OnboardingAssistant created successfully")
        
        # Test basic functionality
        summary = assistant.get_conversation_summary()
        print(f"✅ Conversation summary: {summary}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to create OnboardingAssistant: {e}")
        return False

def test_data_files():
    """Test if required data files exist"""
    print("\nTesting data files...")
    
    try:
        from config import Config
        
        files_to_check = [
            ("Member info", Config.MEMBER_INFO_PATH),
            ("Process info", Config.PROCESSES_INFO_PATH), 
            ("Tech stack info", Config.TECHSTACK_INFO_PATH)
        ]
        
        for name, path in files_to_check:
            if os.path.exists(path):
                print(f"✅ {name} file exists: {path}")
            else:
                print(f"❌ {name} file missing: {path}")
                
    except Exception as e:
        print(f"❌ Error checking data files: {e}")

def main():
    """Run all tests"""
    print("🧪 Running integration tests...\n")
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    # Test assistant creation 
    if not test_assistant_creation():
        success = False
    
    # Test data files
    test_data_files()
    
    print(f"\n{'🎉 All tests passed!' if success else '❌ Some tests failed!'}")
    
    if success:
        print("\n🚀 Ready to run the Streamlit app with:")
        print("   streamlit run app.py")
    else:
        print("\n🔧 Please fix the issues above before running the app.")

if __name__ == "__main__":
    main()
