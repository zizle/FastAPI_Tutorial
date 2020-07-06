# _*_ coding:utf-8 _*_
# Author： zizle
# Created:2020-06-
# ------------------------
import uvicorn
from app.main import app

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
