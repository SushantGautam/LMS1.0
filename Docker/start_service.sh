rm -r /ublrandd/WebApp/migrations
rm -r /ublrandd/quiz/migrations
rm -r /ublrandd/forum/migrations
rm -r /ublrandd/survey/migrations
pip install --prefer-binary -r requirements.txt 
python manage.py makemigrations WebApp forum quiz survey
python manage.py migrate


python manage.py loaddata /ublrandd/WebApp/intial-fixtures-data/initial-fixtures-WebApp.json 
python manage.py loaddata /ublrandd/WebApp/intial-fixtures-data/initial-fixtures-survey.json 
python manage.py loaddata /ublrandd/WebApp/intial-fixtures-data/initial-fixtures-forum.json


python manage.py runserver 0.0.0.0:8000
