#!/usr/bin/env bash

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate

python manage.py shell -c "
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ['ADMIN_USERNAME']
email = os.environ.get('ADMIN_EMAIL', '')
password = os.environ['ADMIN_PASSWORD']
user, created = User.objects.get_or_create(
    username=username,
    defaults={'email': email}
)
user.is_staff = True
user.is_superuser = True
user.set_password(password)
user.save()
print('Admin user ready:', username)
"