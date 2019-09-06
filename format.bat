rmdir /s /q WebApp\migrations
rmdir /s /q quiz\migrations
rmdir /s /q forum\migrations
rmdir /s /q survey\migrations

del db.sqlite3
python manage.py makemigrations WebApp forum quiz survey

python manage.py migrate
python manage.py createsuperuserwithpassword    --username nsdevil --password nsdevil --email admin@example.org    --preserve