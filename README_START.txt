HOW TO START THE SERVER
=======================

Option 1 - Terminal (Recommended):
1. Open Terminal
2. Run: cd ~/Desktop/difficult-conversations-multi-scenario
3. Run: ./run.sh
4. Open browser to: http://localhost:8000
5. Press Ctrl+C to stop server

Option 2 - Background Process:
1. Open Terminal  
2. Run: cd ~/Desktop/difficult-conversations-multi-scenario
3. Run: nohup ./run.sh > server.log 2>&1 &
4. Open browser to: http://localhost:8000
5. To stop: pkill -f "uvicorn agent:app"

The server is currently running at:
http://localhost:8000

OpenAI API Key is configured in run.sh
