# _*_ coding:utf-8 _*_

"""
依赖关系需要是可以可调用的，就像是函数、类,...；
依赖关系的函数参数跟路径操作函数的参数一样的用法

使用依赖关系：
1 Have shared logic (the same code logic again and again).
2 Share database connections.
3 Enforce security, authentication, role requirements, etc.
4 And many other things...
"""
from typing import Optional
from fastapi import APIRouter, Depends, Cookie, Header, HTTPException


router = APIRouter()
# 这个就是被依赖的关系函数
# 被依赖函数可以像路径操作函数一样定义,异步使用async
# FastAPI调用依赖关系会跟调用路径操作函数一样。
# 1 使用函数作为依赖项


async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@router.get("/depend_func/", summary="使用函数作为依赖注入")
async def read_items(commons: dict = Depends(common_parameters)):  # 使用依赖关系
    commons['limit'] += 10
    return commons


# 2 使用类作为依赖项
class CommonQueryParams:
    def __init__(
        self,
        q: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ):
        self.q = q
        self.skip = skip
        self.limit = limit


@router.get("/depend_cls/", summary="使用类作为依赖注入")
async def read_items2(commons: CommonQueryParams = Depends(CommonQueryParams)): # 这里Depends的参数可省略,因为类型名称与依赖类一致
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    response.update({"limit": commons.limit + 10})
    return response


# 3 依赖嵌套(可任意嵌套层)
def query_extractor(q: Optional[str] = None):
    if not q:
        return None
    return q + " in extractor_function"


def query_or_cookie_extractor(
    q: str = Depends(query_extractor),
    last_query: Optional[str] = Cookie(None)
):
    if not q:
        return last_query
    return q


@router.get('/depend_extractor/', summary="嵌套依赖的使用")
async def extractor_depends(query_or_default: str = Depends(query_or_cookie_extractor, use_cache=False)):  # use_cache可以替代同个请求内多次使用依赖的缓存(不缓存),依赖项返回值默认缓存
    return {"q_or_cookie": query_or_default}


# 4 无返回值的依赖项在路径装饰器中使用它
async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


# 可使用多个依赖项
@router.get(
    "/depens_in_decorator/",
    dependencies=[Depends(verify_key),Depends(verify_token)],  # 按顺序执行
    summary="在路径装饰器中使用依赖,类似钩子函数"
)
async def read_items3():
    return [{"item": "Foo"}, {"item": "Bar"}]


# 5 在依赖中使用yield关键字,生成器做依赖
# 在响应response之前只会执行yield语句及之前的代码
async def dependency_a():
    dep_a = "dependency_a"
    try:
        print("进入dependency_A函数")
        yield dep_a
    finally:
        print("关闭dependency_A函数")


async def dependency_b(dep_a=Depends(dependency_a)):
    dep_b = "dependency_b"
    try:
        print("进入dependency_B函数")
        yield dep_b
    finally:
        print("关闭dependency_B函数")


async def dependency_c(dep_b=Depends(dependency_b)):
    dep_c = "dependency_c"
    # 如果使用yield将会收到路径操作函数或其他任何地方的错误,使用try-finally确保最后的执行
    # 在yield之后如果再抛出异常也是会被捕获,使其无法抛出异常；在之前仍然照常使用
    # 如果还想捕获错误，或其他系统错误，需写try...exception代码块
    # 当使用yield关键字作为依赖的时候FastAPI实际上是创建一个上下文管理器
    try:
        print("进入dependency_C函数")
        yield dep_c
    finally:
        print("关闭dependency_C函数")


@router.get("/depend_yield/",summary="嵌套依赖含yield")
async def read_item4(depends_name: str = Depends(dependency_c)):
    return {"message": "嵌套依赖中含yield...", "depends": depends_name}


# 拓展：自定义一个上下文管理器(在FastAPI框架中没什么作用,只是Python知识拓展)
class MySuperContextManager:
    def __init__(self, name: str):
        self.name = name
    
    def __enter__(self):
        print("进入管理器...")

    def __exit__(self, exc_type, exc_value, traceback):
        print("退出管理器...")


@router.get("/my_context_manager/", summary="拓展:自定义上下文管理器")
async def my_content_manager():
    with MySuperContextManager("my_manager") as mscm:
        print("函数结束..")
    return "finished!"

