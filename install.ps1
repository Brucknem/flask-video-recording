python -m virtualenv venv
.\venv\Scripts\activate
python -m pip install -r requirements.txt

flask --app app init-db
flask --app app run --debug