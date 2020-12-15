rm -r WebApp/migrations
rm -r quiz/migrations
rm -r forum/migrations
rm -r survey/migrations

fuser -k -n tcp 9002
rm db.sqlite3
python manage.py makemigrations WebApp forum quiz survey
python manage.py migrate
python manage.py loaddata WebApp/intial-fixtures-data/initial-fixtures-WebApp.json
python manage.py loaddata WebApp/intial-fixtures-data/initial-fixtures-survey.json
python manage.py loaddata WebApp/intial-fixtures-data/initial-fixtures-forum.json

