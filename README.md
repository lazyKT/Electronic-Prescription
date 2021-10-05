## Project Setup
- cd E_Prescription
- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirement.txt

## How to start development server
### For Unix Systems
- cd E_Prescription
- source venv/bin/activate
- export FLASK_APP=wsgi.py
- export FLASK_ENV=development
- flask run
