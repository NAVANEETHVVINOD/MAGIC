@echo off
echo ============================================
echo 🚀 STARTING MAGIC HACKATHON PHOTO BOOTH
echo ============================================
echo.

echo 1. Checking requirements...
pip install -r requirements.txt

echo 2. Starting Camera System Server...
cd camera
start "Magic Booth Server" python camera_main.py

echo 3. Waiting for server to initialize...
timeout /t 5

echo 4. Opening User Interface...
start http://localhost:5000

pause
