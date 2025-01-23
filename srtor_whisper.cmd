@echo off
set /p input=Please enter the folder path: 
python srtor_whisper.py -p "%input%"
pause