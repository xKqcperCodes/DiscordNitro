@echo off
echo Installing required packages...
pip install requests
pip install faker
pip install colorama
pip install datetime
pip install concurrent.futures
echo Installation complete.
py gen.py
pause