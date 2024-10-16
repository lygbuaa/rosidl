@ECHO OFF
SET ENTRY_PATH=%~dp0
ECHO ENTRY_PATH: %ENTRY_PATH%
ECHO input command line: %*
python3 %ENTRY_PATH%\wolfes_cg_main.py %*