FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /ublrandd
WORKDIR /ublrandd
COPY . /ublrandd/

RUN bash -c "pip install --prefer-binary -r requirements.txt"
RUN bash -c "python -m textblob.download_corpora"


RUN bash -c "python manage.py makemigrations WebApp forum quiz survey"
RUN bash -c "python manage.py migrate"
RUN bash -c "python manage.py loaddata /ublrandd/WebApp/intial-fixtures-data/initial-fixtures-WebApp.json  && \
    python manage.py loaddata /ublrandd/WebApp/intial-fixtures-data/initial-fixtures-survey.json  && \
    python manage.py loaddata /ublrandd/WebApp/intial-fixtures-data/initial-fixtures-forum.json"