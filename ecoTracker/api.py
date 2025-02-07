from ninja import NinjaAPI
from .routes import actions, user

api = NinjaAPI(
    title="EcoTrack",
    version="1.0.0",
    description=("API RESTful para incentivar ações sustentáveis"),
)

api.add_router("/auth", user.user_route)
api.add_router("/actions", actions.action_router)
