import secrets
import jwt

# To import JWT settings from project "settings.py" file
from django.conf import settings
JWT_AUTH=settings.JWT_AUTH

def token():
    return str(jwt.encode({'jti':secrets.token_urlsafe(60)}, JWT_AUTH['JWT_SECRET'], algorithm=JWT_AUTH['JWT_ALGORITHM']))[2:-1]