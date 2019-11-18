
@ECHO OFF
FOR /F "tokens=5" %%T IN ('netstat -a -n -o ^| findstr "8000" ') DO (
SET /A ProcessId=%%T) &GOTO SkipLine
:SkipLine
echo ProcessId to kill = %ProcessId%
taskkill /f /pid %ProcessId%


rmdir /s /q WebApp\migrations
rmdir /s /q quiz\migrations
rmdir /s /q forum\migrations
rmdir /s /q survey\migrations

del db.sqlite3

pip install -r requirements.txt
python manage.py makemigrations WebApp forum quiz survey
python manage.py migrate
python manage.py loaddata WebApp\intial-fixtures-data\initial-fixtures-WebApp.json
python manage.py loaddata WebApp\intial-fixtures-data\initial-fixtures-survey.json
python manage.py loaddata WebApp\intial-fixtures-data\initial-fixtures-forum.json
python manage.py runserver 0.0.0.0:8000


