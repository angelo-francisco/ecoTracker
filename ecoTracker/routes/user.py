from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from ninja import Router

from ..auth import create_token
from ..schemas import MessageSchema, UserCreateSchema, UserSchema

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


@user_route.post("/login")
def login(request, username: str, password: str):
    """
    Endpoint de login que autentica o usuário e retorna um token JWT.
    """
    user = authenticate(username=username, password=password)
    if user:
        token = create_token(user)
        return {"token": token}
    return {"error": "Credenciais inválidas"}, 401
