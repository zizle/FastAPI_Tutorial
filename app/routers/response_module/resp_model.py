# _*_ coding:utf-8 _*_
from typing import Optional, Union, List, Dict
from fastapi import APIRouter, File
from pydantic import BaseModel, EmailStr


router = APIRouter()

"""Response模型的使用"""

# 1.1 接收与返回的模型字段需要不一致时

# 用户进入的模型
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None

# 返回信息的模型
class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

exclude_user = {"user_id":{"name": "superuser"}}
@router.post('/user_msg/',
response_model=UserOut, # 指定了返回的模型，就不会按接收的模型字段返回(过滤数据)。
response_model_exclude_unset=True,  # 只显示结果数据中含有的字段，结合exclude_user看,虽然模型有email可数据中没有，就只会返回数据中有的name
response_model_exclude=["email"],  # 可指定相应模型中要排除的那些字段
# response_model_include=["name",]  # 可指定要响应的模型中包含的那些字段
)  
async def user_login(user: UserIn):
    return user


# 1.2 额外模型的使用
class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Optional[str] = None


def fake_password_hasher(raw_password: str):
    return "supersecrect" + raw_password

def fake_save_user(user_in: UserIn):
    hash_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hash_password)
    print("User saved!")
    print(user_in_db)
    return user_in_db

@router.post("/extra_model_save_user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

# 1.3 联合响应模型，它代表响应的结果将会是联合中的任何一个
# 模型也是可继承使用的
class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type = "car"

class PlaneItem(BaseItem):
    type = "plane"
    size: int

@router.get("/union_models/{item_key}/", response_model=Union[CarItem, PlaneItem])
async def union_models(item_key: str):
    items_db = {
        "item1": {"description": "这是item1的一段描述", "type": "car"},
        "item2": {"description": "这是item2的一段描述", "type": "plane", "size":100}
    }
    return items_db[item_key]

# 1.4 返回列表模型
@router.get("/list_response_model/", response_model=List[BaseItem])
async def read_items():
    items = [
        {"type": "Foo", "description": "There comes my hero"},
        {"type": "Red", "description": "It's my aeroplane"},
    ]
    return items

# 1.5 返回任意字典模型
@router.get("/keyword-weights/", response_model=Dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}
