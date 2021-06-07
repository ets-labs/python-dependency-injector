echo on
REM The assumption is made that the python executable can be found.

REM Set variabless
set ENV_NAME=wslenv2-win
set VENV_DIR=%ENV_NAME%\Scripts
set PYTHON_VENV=%VENV_DIR%\python.exe

REM Create virtual environment
python -m venv %ENV_NAME%

REM Populate dependencies and run the example
Start /WAIT cmd /k "%VENV_DIR%\activate&^
%PYTHON_VENV% -m pip install --upgrade pip&^
%PYTHON_VENV% -m pip install -r .\requirements.txt&^
set MOVIE_FINDER_TYPE=csv&^
%PYTHON_VENV% -m movies&^
set MOVIE_FINDER_TYPE=sqlite&^
%PYTHON_VENV% -m movies&^
%VENV_DIR%\deactivate&^
pause

