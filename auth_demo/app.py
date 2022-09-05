from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .adapters import repository
from .service_layer import services

app = FastAPI()

class UserItem(BaseModel):
    name: str
    password: str

class TokenItem(BaseModel):
    token: str

@app.post("/users")
def create_user(user_item: UserItem):
    try:
        services.create_user(user_item.name, user_item.password, repository.MemUserRepository())
    except services.UserExists as e:
        raise HTTPException(status_code=400, detail=str(e))
    return None


@app.delete("/users/{name}")
def delete_user(name: str):
    try:
        services.delete_user(name)
    except services.UserNotExists as e:
        raise HTTPException(status_code=404, detail=str(e))
    return None


@app.post("/roles")
def create_role(name: str):
    try:
        services.create_role(name)
    except services.UserNotExists as e:
        raise HTTPException(status_code=400, detail=str(e))
    return None


@app.delete("/roles/{name}")
def delete_role(name: str):
    try:
        services.create_role(name)
    except services.UserNotExists as e:
        raise HTTPException(status_code=404, detail=str(e))
    return None


@app.post("/users/{user_name}/roles/{role_name}")
def add_role_to_user(user_name: str, role_name: str):
    try:
        services.add_role_to_user(user_name, role_name)
    except (services.UserNotExists, services.RoleExists) as e:
        raise HTTPException(status_code=404, detail=str(e))
    return None


@app.post("/auth-tokens")
def user_auth(user_item: UserItem):
    try:
        token = services.auth_user(UserItem.name, UserItem.password)
    except (services.UserNotExists, services.PasswordError) as e:
        raise HTTPException(status_code=400, detail="auth fail")
    return {"token": token.key}


@app.delete('/auth-tokens')
def invalidate(token_item: TokenItem):
    try:
        services.invalidate_token(token_item.token)
    except services.TokenIvalid as e:
        raise HTTPException(status_code=404, detail="token invalid")
    return None


@app.get('/auth-tokens/{token}/role-checks')
def check_role(token:str, role_name: str):
    try:
        ret = services.check_role(token, role_name, repository.MemRoleRepository())
    except services.TokenIvalid as e:
        raise HTTPException(status_code=400, detail="token invalid")
    return {"result": ret}


@app.get('/auth-tokens/{token}/roles')
def get_token_roles(token: str):
    try:
        ret = services.get_token_roles(token)
    except services.TokenIvalid as e:
        raise HTTPException(status_code=400, detail="token invalid")
    return {"items": ret}


