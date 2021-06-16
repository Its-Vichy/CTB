@echo off
cls
echo CTB Install...
pip install -r requirements.txt
pip install -U requests[socks]
pause
