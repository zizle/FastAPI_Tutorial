# _*_ condig:utf-8 _*_

"""查询参数的使用和验证"""
from typing import Optional, List
from fastapi import APIRouter, Query

router = APIRouter()

# 1 查询参数的使用
@router.get("/read_item/")  # /items/?skip=?&limit=?
async def read_item(skip: int = 0, limit: int = 10):
    fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
    return fake_items_db[skip : skip + limit]

# 2 查询参数的验证
@router.get("/read_items/")
async def read_items(
    q: str = Query(
        ...,  # 参数为必须，声明为None则是可选参数
        min_length=3  # 最小需3个字符
        ),
    # p为并列查询参数
    p: Optional[List[str]] = Query(
        ["default"],  # 参数的默认值，None则为非必须
        alias='p-hahaha',  # 查询参数的别名，客户端需用这个名称
        )
    ):
    results = {"items":[{"name": "Item Foo"}, {"name": "Item 第二个项"}]}
    if q:
        results.update({"q": q})
    results.update({"p": p}) 
    return results

# 3 查询参数的使用和路径参数的使用可以混合起来使用。
@router.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
