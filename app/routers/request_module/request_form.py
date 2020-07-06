# _*_ coding: utf-8 _*_

from fastapi import APIRouter, Form
from pydantic import BaseModel


router = APIRouter()

# Form表单的接收和验证
@router.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}
