from typing import Union
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel

from .adapters import repository
from .service_layer import services

app = FastAPI()


class UserItem(BaseModel):
    name: str
    password: str


class RoleItem(BaseModel):
    name: str


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
        services.delete_user(name, repository.MemUserRepository())
    except services.UserNotExists as e:
        raise HTTPException(status_code=404, detail=str(e))
    return None


@app.post("/roles")
def create_role(role_item: RoleItem):
    try:
        services.create_role(role_item.name, repository.MemRoleRepository())
    except services.RoleExists as e:
        raise HTTPException(status_code=400, detail=str(e))
    return None


@app.delete("/roles/{name}")
def delete_role(name: str):
    try:
        services.delete_role(name, repository.MemRoleRepository())
    except services.RoleNotExists as e:
        raise HTTPException(status_code=404, detail=str(e))
    return None


@app.post("/users/{name}/roles")
def add_role_to_user(name: str, role_item: RoleItem):
    try:
        services.add_role_to_user(name, role_item.name,
                                  repository.MemUserRepository(),
                                  repository.MemRoleRepository())
    except (services.UserNotExists, services.RoleNotExists) as e:
        raise HTTPException(status_code=400, detail=str(e))
    return None


@app.post("/auth-tokens", summary='Authenticate')
def user_auth(user_item: UserItem):
    try:
        token = services.auth_user(user_item.name, user_item.password,
                                   repository.MemUserRepository())
    except (services.UserNotExists, services.PasswordError) as e:
        raise HTTPException(status_code=400, detail="auth fail")
    return {"token": token.key}


@app.delete('/auth-tokens/{token}')
def invalidate(token: str):
    try:
        services.invalidate_token(token)
    except services.TokenIvalid as e:
        raise HTTPException(status_code=404, detail="token invalid")
    return None


@app.get('/auth-tokens/{token}/role-checks/{role_name}')
def check_role(token:str, role_name: str):
    try:
        ret = services.check_role(token, role_name, repository.MemRoleRepository())
    except (services.TokenIvalid, services.RoleNotExists) as e:
        raise HTTPException(status_code=400, detail="token invalid")
    return {"result": ret}


@app.get('/auth-tokens/{token}/roles', summary='All Roles')
def get_token_roles(token: str):
    try:
        ret = services.get_token_roles(token)
    except services.TokenIvalid as e:
        raise HTTPException(status_code=400, detail="token invalid")
    return {"items": ret}

