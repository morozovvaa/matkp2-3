@echo off
pyinstaller --onefile --add-data "sounds:sounds" --add-data "images:images" main.py
pause
