from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from p123 import P123Client, check_response
import logging
import os

# 初始化日志
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# 增强参数校验
def validate_payload(parts: list) -> dict:
    if len(parts) < 3:
        raise ValueError("URI 格式错误")
    
    try:
        return {
            "FileName": parts[0],
            "Size": int(parts[1]),
            "Etag": parts[2].split("?")[0].lower(),  # 强制小写
            "S3KeyFlag": parts[2].split("?")[1] if "?" in parts[2] else ""
        }
    except ValueError as e:
        raise ValueError(f"无效的参数格式: {str(e)}")

client = P123Client(
    passport=os.getenv("P123_PASSPORT"),
    password=os.getenv("P123_PASSWORD")
)
client.login()

app = FastAPI()

@app.get("/{uri:path}")
async def index(request: Request, uri: str):
    try:
        logger.info(f"收到请求: {request.url}")
        
        # 增强参数校验
        parts = uri.split("|")
        payload = validate_payload(parts)
        
        # 调试日志
        logger.debug(f"解析后的参数: {payload}")
        
        # 获取下载链接
        raw_resp = client.download_info(payload)
        logger.debug(f"原始响应: {raw_resp}")
        
        validated_resp = check_response(raw_resp)
        download_url = validated_resp["data"]["DownloadUrl"]
        
        logger.info(f"重定向至: {download_url}")
        return RedirectResponse(download_url, status_code=302)
    
    except Exception as e:
        logger.error(f"处理失败: {str(e)}", exc_info=True)
        return JSONResponse(
            {"state": False, "message": str(e)},
            status_code=500 if isinstance(e, ValueError) else 400
        )
