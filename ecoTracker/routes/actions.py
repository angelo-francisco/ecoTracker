from typing import List
from uuid import UUID

from django.db.models import Sum
from ninja import Router

from ..auth import jwt_auth
from ..models import Action
from ..schemas import (
    ActionCreateOrUpdateSchema,
    ActionSchema,
    MessageSchema,
)

action_router = Router(tags=["Actions"], auth=jwt_auth)


@action_router.post("/create", response=ActionSchema)
def create_action(request, payload: ActionCreateOrUpdateSchema):
    """
    Cria uma nova ação sustentável para o usuário autenticado.
    """
    user = request.auth
    action = Action.objects.create(
        title=payload.title,
        description=payload.description,
        category=payload.category,
        points=payload.points,
        user=user,
    )
    return action


@action_router.get("/list", response=List[ActionSchema])
def list_actions(request):
    """
    Lista todas as ações sustentáveis cadastradas pelo usuário autenticado.
    """
    user = request.auth
    actions = Action.objects.filter(user=user)
    return actions


@action_router.get(
    "/get/{action_id}",
    response={200: ActionSchema, 404: MessageSchema},
)
def get_action(request, action_id: UUID):
    """
    Retorna os detalhes de uma ação sustentável específica.
    """
    action = Action.objects.filter(id=action_id).first()
    if not action:
        return 404, {"message": "Ação não encontrada", "type": "error"}
    return 200, action


@action_router.put(
    "/update/{action_id}",
    response={200: ActionSchema, 404: MessageSchema},
)
def update_action(request, action_id: UUID, payload: ActionCreateOrUpdateSchema):
    """
    Atualiza os dados de uma ação sustentável existente.
    """
    action = Action.objects.filter(id=action_id).first()

    if not action:
        return 404, {"message": "Ação não encontrada", "type": "error"}

    action.title = payload.title
    action.description = payload.description
    action.category = payload.category
    action.points = payload.points

    action.save()
    return 200, action


@action_router.delete(
    "/del/{action_id}",
    response={200: MessageSchema, 404: MessageSchema},
)
def delete_action(request, action_id: UUID):
    """
    Exclui uma ação sustentável específica.
    """
    action = Action.objects.filter(id=action_id).first()

    if not action:
        return 404, {"message": "Ação não encontrada", "type": "error"}

    action.delete()
    return 200, {"message": "Ação deletada com sucesso!", "type": "success"}


@action_router.get(
    "/total-points",
)
def get_user_points(request):
    """
    Endpoint que retorna o total de pontos das ações registradas.
    """
    user = request.auth

    total_points = Action.objects.filter(user=user).aggregate(
        total_points=Sum("points")
    )["total_points"]

    return {"total_points": total_points or 0}
