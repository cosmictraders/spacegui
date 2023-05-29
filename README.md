# Spacegui
A GUI for spacetraders, built with `autotraders`, `flask`, and `bootstrap`
## Getting Started
Run to install the requirements
`pip install -r requirements.txt`

To run the website use `python run.py` if you are on windows
or don't want one of the servers below.

## Gunicorn
`gunicorn wsgi:app`
One worker should really be enough.

You will be automatically redirected to a setup page when you visit `localhost:5000` (or port `8000` if using gunicorn)
