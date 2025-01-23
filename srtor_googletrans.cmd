@echo off
set /p input=Please enter the folder path: 
python srtor_googletrans.py -p "%input%"
pause