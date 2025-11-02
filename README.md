# Employee Portal (Render-ready)
Minimal Django app with login + dashboard and signed auto-login endpoint.

## Deploy on Render
1. Push to GitHub.
2. Render Web Service:
   - Build: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
   - Start: gunicorn employee_portal.wsgi
3. Env Vars:
   - SECRET_KEY = (random)
   - DEBUG = False
   - AUTOLOGIN_SHARED_SECRET = (match client script)
   - ALLOWED_HOSTS = your-service.onrender.com
