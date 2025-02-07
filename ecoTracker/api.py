from django.contrib.auth import authenticate
from ninja import NinjaAPI
from ninja.security import HttpBearer

from .auth import check_token, create_token

api = NinjaAPI(
    title="EcoTrack",
    version="1.0.0",
    description="Uma api sustentável para gerir acções sustentáveis",
)


class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        return check_token(token)


jwt_auth = JWTAuth()


@api.post("/login")
def login(request, username: str, password: str):
    """Autenticação de usuário e geração de JWT"""
    user = authenticate(username=username, password=password)
    if user:
        token = create_token(user)
        return {"token": token}
    return {"error": "Credenciais inválidas"}, 401


@api.get("/protegido", auth=jwt_auth)
def protegido(request):
    """Rota protegida por JWT"""
    return {"message": f"Bem-vindo, {request.auth.username}!"}


@api.get("/test")
def test(request):
    return {"msg": test}
