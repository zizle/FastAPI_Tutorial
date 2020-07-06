# _*_ coding:utf-8 _*_

from fastapi import APIRouter, File, UploadFile, Form

router = APIRouter()

# 1 字节型接收文件
@router.post("/files/")
async def create_file(file: bytes = File(...)):
    # 多文件使用 files: List[bytes] = File(...)
    return {"file_size": len(file)}

# 2文件型接收文件
@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # 多文件使用 files: List[UploadFile] = File(...)

    # file有以下属性：`filename`,`content_type`,`file`(SpooledTemporaryFile类文件对象)
    # file有以下异步方法：write(data) 写入str or bytes 到file中
    #                    read(size): Reads size (int) bytes/characters of the file.
    #                    seek(offset): Goes to the byte position offset (int) in the file.
    #                    close(): Closes the file.
    return {"filename": file.filename}


# 3 文件和表单的混合使用
# summary - API文档中路径后的说明
# deprecated = True - API 文档中显示本接口已弃用
@router.post(
    "/form_with_file/",
    summary="使用FormData上传文件和Form表单",
    deprecated=True,
    response_description="这里是写返回的数据说明文档"
)
async def form_with_file(
    file: bytes = File(...),
    file2: UploadFile = File(...),
    notes: str = Form(...)
):
    """
    **注释：** 这里的注释会出现的API说明文档中
    """
    return {
        "file_size": len(file),
        "file2_content_type": file2.content_type,
        "notes": notes
    }
