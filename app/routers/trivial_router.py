# _*_ coding:utf-8 _*_

from fastapi import APIRouter
from .trivial import json_convert, use_dependencies, cors_request
router = APIRouter()

router.include_router(use_dependencies.router, prefix="/dependencies")  # 使用依赖注入
router.include_router(json_convert.router, prefix="/json_convert")  # json兼容编码器
router.include_router(cors_request.router, prefix="/cors")  # 跨域请求设置见main.py

