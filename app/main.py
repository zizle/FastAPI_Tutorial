# _*_ coding:utf-8 _*_
import time
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .routers import request_router, response_router, trivial_router

# 设置文档的一些元数据配置
# 2 设置标签的配置
tags_metadata = [
    {
        "name": "其余功能",
        "description": "除Request和Response之外其他琐碎功能使用",
        "externalDocs": {
            "description": "官方FastAPI文档",
            "url": "https://fastapi.tiangolo.com/",
        },
    }
]

# 1 设置标题等
app = FastAPI(
    title="FastAPI教程项目",
    description="学习FastAPI的用户指南",
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/apis",  # API文档的路径
    redoc_url=None
)

# 挂载静态文件路径
app.mount("/static", StaticFiles(directory="statics"), name="static")


async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="x-token错误...")

# 其他功能
app.include_router(
    trivial_router.router,
    prefix="/trivial",
    tags=["其余功能"]
)


# 响应相关
app.include_router(
    response_router.router,
    prefix="/response",
    tags=["响应Response使用"],
    responses={404:{"description": "Not Found"}},
    #dependencies=[Depends(get_token_header)],  # 依赖，类似于钩子函数
)
# 请求相关
app.include_router(request_router.router, prefix="/request", tags=["请求Request使用"])


"""中间件的使用"""
# 1 中间件在请求之前和返回response之前都会执行一次
# 2 含有yield的依赖，依赖中的后续代码执行于中间件之后

# 中间件使用例子:记录本次请求的消耗时间,将信息放在头部返回
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# 使用CORS中间件实现跨域资源访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8848"],
    allow_credentials=True,  # 指示跨域请求支持cookies
    allow_methods=["*"],
    allow_headers=["*"]
)
