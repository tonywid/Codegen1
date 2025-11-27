@echo off
echo -----------------------------
echo start Codegen1.py - generate source-code
echo -----------------------------
@rem search for 'todo'
@rem -----------------------------
rem --- todo: set environment-parameters:
rem xxxdir .. need to be set
rem "C:\Users\a813672\OneDrive - Erste Group\Wdd-Source\Wd-Python-Source\wdenv2\Scripts\python.exe" "C:\Users\a813672\OneDrive - Erste Group\Wdd-Workspaces\PyCharm\Codegen1\Codegen1.py"
set PYTHONPATH=C:\Users\a813672\OneDrive - Erste Group\Wdd-Workspaces\PyCharm\WdStdPy
set venvdir="C:\Users\a813672\OneDrive - Erste Group\Wdd-Source\Wd-Python-Source\wdenv2\Scripts"
set scriptdir="C:\Users\a813672\OneDrive - Erste Group\Wdd-Workspaces\PyCharm\Codegen1"
@echo on
dir %pythonpath%
@rem -----------------------------
@rem --- todo: set commandline-parameters:
@rem inifile .. the ini-file
%venvdir%\python.exe %scriptdir%\exp_diverse.py
@echo off
echo -----------------------------
echo end of bat
echo -----------------------------
pause
