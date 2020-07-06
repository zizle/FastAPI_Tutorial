# _*_ coding:utf-8 _*_
from enum import Enum
from typing import Optional
from fastapi import APIRouter, Path, Query

router = APIRouter()

"""路径参数的验证使用"""

# 1 路径参数的类型
@router.get("/{item_key}/")
async def read_item(item_key: str):  # 路径中item_key只能是string,FastAPI会转换int与string
    return {"name":"Fake Specific Item", "item_id": item_key}


# 2 路径参数的顺序
@router.get("/users/me")  # 这个必须写在前面，否则将被下面的user_id匹配
async def read_user_me():
    return {"user_id": "the current user"}

@router.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# 3 可用枚举类型设置有效的路径参数值，除枚举外的参数将不可用
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@router.get("/model/{model_name}/")  # model_name的值只能是ModelName枚举中的值
async def get_model(model_name: ModelName):  # 声明路径参数
    if model_name == ModelName.alexnet:  # 可直接枚举类.值来取值
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet": # 可用枚举模型对应的参数.value取值
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

# 4 匹配路径的路径参数
@router.get("/files/{file_path:path}")  # 使用:path来匹配含路径的路径参数
async def read_file(file_path: str):
    return {"file_path": file_path}

# 5 路径参数的验证
@router.get("/auth_path_params/{item_id}/")
async def path_params_items(
    item_id: int = Path(
        ...,
        title="The ID of item to get",
        ge=10,  # ge 大于等于,gt大于
        le=100,  # le 小于等于,lt小于
    ),
    q: str  = Query(None, alias="item-query"),
    size: float = Query(1, gt=0, lt=15)
):
    items_db = [{"id": 1, "name": "项目1"}, {"id": 2, "name":"项目2"}]
    if q:
        items_db.append({"item_q": q})
    return items_db

# 6 查询参数中的【弃用参数】-该参数已弃用，但又需要保留一阵子的情况(旧版客户端或其他客户端在使用)
@router.get("/deprecated/")
async def deprecated_params(
    q: Optional[str] = Query(
        None,  # 声明参数是否必须
        alias="item-query",  # 参数别名
        title="Query Param 标题",  # 参数标题，不知道啥用
        description="查询参数已弃用",  # 文档展示描述
        min_length=3,  # 最低要求长度
        max_length=10,  # 最大限制长度
        regex="^nice$",  # 起始和结尾匹配
        deprecated=True  #  文档展示参数已弃用
    )
):
    items_db = [{"id": 1, "name": "项目1"}, {"id": 2, "name":"项目2"}]
    if q:
        items_db.append({"item_q": q})
    return items_db