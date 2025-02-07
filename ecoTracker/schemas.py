from datetime import datetime
from uuid import UUID

from ninja import Schema


class ActionSchema(Schema):
    id: UUID
    title: str
    description: str
    category: str
    points: int
    created_at: datetime
    user_id: int


class ActionCreateOrUpdateSchema(Schema):
    title: str
    description: str
    category: str
    points: int


class MessageSchema(Schema):
    message: str
    type: str


class UserCreateSchema(Schema):
    username: str
    password: str
    email: str = None


class UserSchema(Schema):
    id: int
    username: str
    email: str = None
