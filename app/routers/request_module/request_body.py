# _*_ coding: utf-8 _*_

"""请求体的使用"""

# _*_ coding:utf-8 _*_
from typing import Optional, List, Set
from datetime import datetime, time, timedelta
from uuid import UUID
from fastapi import APIRouter, Body
from pydantic import BaseModel, Field, HttpUrl


router = APIRouter()

"""1 在模型中验证请求体"""

# 1.1 模型中验证

class LearnerItem(BaseModel):
    name: str
    description: Optional[str] = Field(
        None,
        title="这title我也不知道有啥用",
        max_length=100
    )
    age: int = Field(..., gt=0, description="The age must be greater than zero")
    score: Optional[float] = 0.0

@router.put('/')
async def add_learns(
    learner: LearnerItem = Body(
        ...,  # 表示参数请求体为必须
        example={ # 这个example是在API文档中默认显示的请求体
           "name": "The Learner Name",
           "description": "这是一个描述体",
           "age": 20,
           "score":99.5 
        },
        embed=True,  # 以`learner`为key嵌入到请求体中
        )
):
    learns_db = [{"name":"姓名1","age": 10}, {"name": "姓名2", "age": 20}]
    learns_db.append(learner)
    return learns_db


# 1.2 嵌套请求体

class Image(BaseModel):
    url: HttpUrl  # 检查一个有效的httpUrl,并在Json schema / OpenAPI中进行记录
    name: str

class LearnerItem2(BaseModel):
    name: str
    description: Optional[str] = Field(
        None,
        title="这title我也不知道有啥用",
        max_length=100
    )
    age: int = Field(..., gt=0, description="The age must be greater than zero")
    score: Optional[float] = 0.0
    tags0: list      = []  # 内置列表类型
    tags1: List[str] = []  # 列表指定元素都为string
    tags2: Set[str]  = set()  # 集合类型元素都为string
    image: Image = None  # 嵌套子模型
    images: List[Image] = []  # 嵌套子模型列表


@router.put('/embed_learn/')
async def add_learns(
    learner: LearnerItem2 = Body(
        ...,  # 表示参数请求体为必须
        embed=True,  # 以`learner`为key嵌入到请求体中
        )
):
    learns_db = [{"name":"姓名1","age": 11}, {"name": "姓名2", "age": 22}]
    learns_db.append(learner)
    return learns_db



# 1.3 额外的其他参数类型验证

@router.put("/extra_params/{item_id}")
async def extra_params(
    item_id: UUID,
    start_datetime: Optional[datetime] = Body(None),
    end_datetime: Optional[datetime] = Body(None),
    repeat_at: Optional[time] = Body(None),
    process_after: Optional[timedelta] = Body(None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }
