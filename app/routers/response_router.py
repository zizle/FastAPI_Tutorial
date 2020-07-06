# _*_ coding:utf-8 _*_ 

from fastapi import APIRouter
from .response_module import resp_model, resp_status

router = APIRouter()

router.include_router(resp_model.router, prefix="/response_model")  # 响应使用模型
router.include_router(resp_status.router, prefix="/status_code")  # 响应状态和异常处理
