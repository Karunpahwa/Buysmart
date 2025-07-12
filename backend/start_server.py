#!/usr/bin/env python3
"""
Startup script for BuySmart backend server
Checks for existing processes and starts cleanly
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

def kill_existing_processes():
    """Kill any existing uvicorn processes"""
    try:
        # Kill uvicorn processes
        subprocess.run(["pkill", "-f", "uvicorn"], check=False)
        time.sleep(1)
        print("✓ Killed existing uvicorn processes")
    except Exception as e:
        print(f"Warning: Could not kill existing processes: {e}")

def check_port_available(port=8000):
    """Check if port is available"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('localhost', port))
        sock.close()
        return True
    except OSError:
        return False

def main():
    # Ensure we're in the backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    print("🚀 Starting BuySmart Backend Server...")
    
    # Kill existing processes
    kill_existing_processes()
    
    # Check if port is available
    if not check_port_available(8000):
        print("❌ Port 8000 is still in use. Please wait a moment...")
        time.sleep(2)
        if not check_port_available(8000):
            print("❌ Port 8000 is still busy. Please manually kill processes and try again.")
            sys.exit(1)
    
    print("✓ Port 8000 is available")
    
    # Start uvicorn
    cmd = [
        "uvicorn", 
        "app.main:app", 
        "--reload", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ]
    
    print(f"Starting server with: {' '.join(cmd)}")
    print("Press Ctrl+C to stop the server")
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 