rmdir /s /q WebApp\migrations
rmdir /s /q quiz\migrations
rmdir /s /q forum\migrations
rmdir /s /q survey\migrations

del db.sqlite3

pip install -r requirements.txt
python manage.py makemigrations WebApp forum quiz survey

python manage.py migrate
python manage.py createsuperuserwithpassword    --username nsdevil --password nsdevil --email admin@example.org    --preserve
start /B python manage.py runserver 0.0.0.0:8000
pytest


