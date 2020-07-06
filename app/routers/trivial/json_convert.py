# _*_ coding:utf-8 _*_
from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


router = APIRouter()

#1 json兼容编码器

class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Optional[str] = None


@router.post("/json_convert/")
async def create_item(item: Item):
    items_db = {}
    # print(item, type(item))
    json_compatible_item_data = jsonable_encoder(item)  # 将验证过得到的对象转换为json格式的数据，对象内的datetime数据对象转为str
    # print(json_compatible_item_data, type(json_compatible_item_data))
    items_db["new"] = json_compatible_item_data
    return items_db

#2 body的更新、
class Item2(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5
    tags: List[str] = []


@router.put("/update_body/{item_key}/", summary="put方法body的更新")
async def update_item(item_key: str, item: Item2):
    items = {
        "foo": {"name": "Foo", "price": 50.2},
        "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
        "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
    }
    items[item_key] = jsonable_encoder(item) 
    return items[item_key]

@router.patch("/patch_update/{item_key}/", summary="patch方法body更新")
async def update_item2(item_key: str, item: Item2):
    items = {
        "foo": {"name": "Foo", "price": 50.2},
        "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
        "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
    }
    stored_item_data = items[item_key]
    stored_item_model = Item2(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    update_item = stored_item_model.copy(update=update_data)
    items[item_key] = jsonable_encoder(update_item)
    return items[item_key]
