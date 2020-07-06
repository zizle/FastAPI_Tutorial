# _*_ coding:utf-8 _*_

"""cookie的使用"""

from fastapi import APIRouter, Cookie, Header


router = APIRouter()

# 1.1 接收cookie参数
@router.get("/")
async def read_items(
    *,  # 之后的参数必须以key=value值的形式传入
    item_str: str = Cookie(None)  # 客户端请求头部中的Cookie的item_str为key的值会被读取，cookie中的键值对用;隔开
):
    items_db = {"item1": "项目一"}
    if item_str:
        items_db.update({"item_cookie": item_str})
    return items_db

# 1.2 头部参数的验证

@router.get("/auth_headers/")
async def auth_header_params(
    *,
    user_agent: str = Header(None),  # `user_agent`是个关键字，会读取浏览器的User-Agent
    users_agent: str = Header(
        None,
        convert_underscores=False, # 自定义的头部key,下划线连接的，在返回的头部信息中会转成users-agent,此参数可关闭这个转换
    ),
):
    items_db = {"item1": "项目二"}
    if user_agent:
        items_db.update({"browser": user_agent})
    if users_agent:
        items_db.update({"mydefine": users_agent})
    return items_db
