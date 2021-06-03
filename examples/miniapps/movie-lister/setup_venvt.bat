echo on
set PYTHON37=%UserProfile%\AppData\Local\Programs\Python\Python37\python.exe

REM set variabless
set ENV_NAME=wslenv2-win
set VENV_DIR=%ENV_NAME%\Scripts
set PYTHON_VENV=%VENV_DIR%\python.exe

REM cleanup
rd /s /q %ENV_NAME%

%PYTHON37% -m venv %ENV_NAME%

Start /WAIT cmd /k "%VENV_DIR%\activate & %PYTHON_VENV% -m pip install --upgrade pip & %PYTHON_VENV% -m pip install -r .\requirements.txt & %VENV_DIR%\deactivate & pause & exit 0"

REM MOVIE_FINDER_TYPE=csv
REM MOVIE_FINDER_TYPE=sqlite
