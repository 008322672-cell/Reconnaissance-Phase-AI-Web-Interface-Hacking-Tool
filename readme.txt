to run, put this in terminal
cd C:\Projects\websec-tool
# allow activation just for this terminal session
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
. .\.venv\Scripts\Activate.ps1      # note: dot space
python -m pip show requests         # should print info; if not, install:
python -m pip install -r requirements.txt
python app.py
