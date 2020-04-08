source venv/bin/activate
python manage.py collectstatic
systemctl restart gunicorn
systemctl restart nginx