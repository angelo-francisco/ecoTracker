from datetime import datetime

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from ninja import Body, Router
from ninja.responses import Response

from ..auth import create_token
from ..schemas import MessageSchema, TokenSchema, UserCreateSchema, UserSchema

user_route = Router(tags=["Users"])


@user_route.post("/register", response={201: UserSchema, 400: MessageSchema})
def register(request, data: UserCreateSchema):
    """
    Endpoint para registro de um novo usuário.
    Retorna os dados do usuário cadastrado ou uma mensagem de erro caso o usuário já exista.
    """
    if User.objects.filter(Q(username=data.username) | Q(email=data.email)).exists():
        return 400, {"message": "Usuário já existe", "type": "error"}
    user = User.objects.create_user(
        username=data.username, password=data.password, email=data.email
    )
    return 201, user


@user_route.post("/login", response={200: TokenSchema, 401: MessageSchema})
def login(request, data: dict = Body(...)):
    """
    Endpoint de login que autentica o usuário e retorna um token JWT.
    """
    username = data.get("username")
    password = data.get("password")

    user = authenticate(username=username, password=password)
    if user:
        token = create_token(user)
        response = Response({"token": token})

        response.set_cookie(
            "access_token",
            token,
            httponly=True,
            secure=True,
            max_age=3600,
            samesite="Lax",
        )

        return response
    return 401, {"message": "Credenciais inválidas", "type": "error"}


@user_route.get("/check", response={200: MessageSchema, 400: MessageSchema})
def check_user_is_authenticated(request):
    """
    Endpoint que verifica se o usuário está logado.
    Verifica se o token existe e se é válido.
    """
    token = request.COOKIES.get("access_token")
    print(token)
    if not token:
        return Response({"message": "Usuário não está autenticado", "type": "error"}, status=400)

    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        
        expiration_time = datetime.fromtimestamp(decoded_token['exp'])
        if expiration_time < datetime.now():
            return Response({"message": "Token expirado", "type": "error"}, status=400)
        return Response({"message": "Usuário autenticado", "type": "success"}, status=200)
    
    except jwt.ExpiredSignatureError:
        return Response({"message": "Token expirado", "type": "error"}, status=400)
    
    except jwt.InvalidTokenError:
        return Response({"message": "Token Inválido", "type": "error"}, status=400)
    
    except Exception as e:
        return Response({"message": f"An error occurred: {str(e)}", "type": "error"}, status=500)