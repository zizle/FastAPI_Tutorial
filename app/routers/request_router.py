# _*_ coding:utf-8 _*_ 

from fastapi import APIRouter
from .request_module import path_params, query_params, request_body, use_cookies, request_form, request_file

router = APIRouter()

router.include_router(path_params.router, prefix="/path_params")  # 路径参数
router.include_router(query_params.router, prefix="/query_params")  # 查询参数
router.include_router(request_body.router, prefix="/r_body")  # 请求体
router.include_router(use_cookies.router, prefix="/cookies")  # cookie的使用
router.include_router(request_form.router, prefix="/form")  # Form表单的使用
router.include_router(request_file.router, prefix="/file") # file的上传使用
