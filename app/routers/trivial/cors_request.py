# _*_ coding:utf-8 _*_

# 测试跨域访问

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def cors_request():
    db_items = [{"name":"哈哈", "age": 1}, {"name": "嘿嘿", "age": 2}]
    return db_items

