
# Electronic Prescription System
*An online platform for medical prescriptions.*
## Project Setup
**Prerequisites**
- Python3
- [pip](https://pip.pypa.io/en/stable/installation/)
- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [VirtualEnv](https://virtualenv.pypa.io/en/latest/installation.html#via-pip)
### Windows
- mkdir E_Prescription
- cd E_Prescription
- `git clone https://github.com/lazyKT/Electronic-Prescription.git`
- python3 -m venv venv
- venv\bin\activate
- pip install -r requirement.txt
### Unix
- mkdir E_Prescription
- cd E_Prescription
- `git clone https://github.com/lazyKT/Electronic-Prescription.git`
- python3 -m venv venv
- source venv\bin\activate
- pip install -r requirement.txt

## How to start development server
### For Windows
- cd E_Prescription
- ./venv/Scripts/activate.exxe
- set FLASK_APP=wsgi.py
- set FLASK_ENV=development
- flask run
### For Unix Systems
- cd E_Prescription
- source venv/bin/activate
- export FLASK_APP=wsgi.py
- export FLASK_ENV=development
- flask run

*Then run, http://127.0.0.1:5000 on browser*
