py -m pip install -r requirements.txt
cd src || exit
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
