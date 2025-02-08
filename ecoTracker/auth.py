import jwt
import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from ninja.security import HttpBearer


def create_token(user):
    """Gera um token JWT para o usuário"""
    now = datetime.datetime.utcnow()
    payload = {
        "id": user.id,
        "exp": now + datetime.timedelta(days=1),
        "iat": now, 
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def check_token(token: str):
    """Decodifica e verifica o JWT"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = User.objects.get(id=payload["id"])
        return user
    except (jwt.ExpiredSignatureError, jwt.DecodeError, ObjectDoesNotExist):
        return None


class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        return check_token(token)


jwt_auth = JWTAuth()
