#!/usr/bin/env python3
"""
Startup script for the Employee Onboarding Chatbot
This script will check dependencies and start the Streamlit app
"""

import subprocess
import sys
import os

def check_requirements():
    """Check if all required packages are installed"""
    print("📦 Checking requirements...")
    
    try:
        requirements_file = "requirements.txt"
        if not os.path.exists(requirements_file):
            print(f"❌ {requirements_file} not found")
            return False
        
        # Try to import key packages
        import streamlit
        import openai
        print("✅ All required packages are installed")
        return True
        
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False

def check_config():
    """Check if configuration is properly set up"""
    print("⚙️  Checking configuration...")
    
    try:
        from config import Config
        
        # Check if essential config values are set
        if not Config.OPENAI_ENDPOINT:
            print("❌ OPENAI_ENDPOINT not configured")
            return False
        
        if not Config.OPENAI_API_KEY:
            print("❌ OPENAI_API_KEY not configured")
            return False
            
        if not Config.OPENAI_DEPLOYMENT_NAME:
            print("❌ OPENAI_DEPLOYMENT_NAME not configured")
            return False
        
        print("✅ Configuration looks good")
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def run_app():
    """Start the Streamlit application"""
    print("🚀 Starting the Employee Onboarding Assistant...")
    print("   Opening in your default browser...")
    print("   Press Ctrl+C to stop the application")
    print("-" * 60)
    
    try:
        # Run streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    """Main startup function"""
    print("🧑‍💼 Employee Onboarding Assistant")
    print("=" * 40)
    
    # Check dependencies
    if not check_requirements():
        print("\n🔧 Please install missing requirements and try again")
        sys.exit(1)
    
    # Check configuration
    if not check_config():
        print("\n🔧 Please check your configuration in config.py and try again")
        sys.exit(1)
    
    # Run the app
    run_app()

if __name__ == "__main__":
    main()
