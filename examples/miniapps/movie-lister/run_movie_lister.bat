echo on
set PYTHON37=%UserProfile%\AppData\Local\Programs\Python\Python37\python.exe

REM set variabless
set ENV_NAME=wslenv2-win
set VENV_DIR=%ENV_NAME%\Scripts
set PYTHON_VENV=%VENV_DIR%\python.exe

Start /WAIT cmd /k "%VENV_DIR%\activate & cd & %PYTHON_VENV% data/fixtures.py & set MOVIE_FINDER_TYPE=sqlite & %PYTHON_VENV% -m movies & %VENV_DIR%\deactivate & pause & exit 0"

REM MOVIE_FINDER_TYPE=csv	
REM MOVIE_FINDER_TYPE=sqlite
