"""
Simple script to start the dashboard backend
"""
import os
import sys

def main():
    print("🚀 Starting Brent Oil Price Dashboard...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: app.py not found!")
        print("Please run this script from the dashboard directory")
        sys.exit(1)
    
    # Check if virtual environment exists
    if not os.path.exists('venv'):
        print("🔧 Creating virtual environment...")
        os.system('python -m venv venv')
        print("✅ Virtual environment created")
    
    # Activate virtual environment and install dependencies
    print("📦 Installing dependencies...")
    os.system('.\\venv\\Scripts\\activate && pip install -r requirements.txt')
    
    # Start the Flask app
    print("🌐 Starting Flask backend...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("🧪 Test page available at: http://localhost:5000/test")
    print("=" * 50)
    print("Press Ctrl+C to stop the server")
    
    # Start Flask app
    os.system('.\\venv\\Scripts\\activate && python app.py')

if __name__ == '__main__':
    main()
