# _*_ coding:utf-8 _*_

from fastapi import APIRouter, status, HTTPException, Request
from fastapi.responses import JSONResponse

router = APIRouter()

"""响应状态"""

@router.get("/", status_code=200)
async def read_item():
    return {"item": "itemname"}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}


"""异常处理"""

# 2.1 抛出异常
@router.get("/exception/{item_id}/")
async def read_item1(item_id: str):
    items = {"foo": "The Foo Wrestlers"}
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}

# 2.2 异常中自定义头部信息
@router.get("/exception/my-header/{item_id}/")
async def read_item2(item_id: str):
    items = {"foo": "The Foo Wrestlers"}
    if item_id not in items:
        raise HTTPException(
            status_code=404, 
            detail="My Define Response Header",
            headers={"X-Error": "There goes my error"}
    )
    return {"item": items[item_id]}

# 2.3 自定义异常类 (APIRouter中没有`exception_handler`方法,FastAPI中才有,这种使用方法在app中才能使用)
# class UnicornException(Exception):
#     def __init__(self, description: str):
#         self.description = description


# @router.exception_handler(UnicornException)  # 传入的是框架内部的异常类，则是重写异常处理
# async def unicorn_exception_handler(request: Request, exec: UnicornException):
#     return JSONResponse(
#         status_code=418,
#         content={"message": f"Oops! {exec.name} did something."}
#     )


# @router.get("/exception/unicorn/")
# async def read_unicorn(description: str):
#     if description != "yolo":
#         raise UnicornException(description=description)
#     return {"unicorn_description": description}

