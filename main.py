from fastapi import FastAPI, Request
from p123 import P123Client, check_response
from contextlib import asynccontextmanager
import logging
import os

# 日志配置
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# 全局客户端实例
client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    global client
    try:
        # 初始化客户端
        client = P123Client(
            passport=os.getenv("P123_PASSPORT"),
            password=os.getenv("P123_PASSWORD"),
            auto_reconnect=True  # 假设 SDK 支持断线重连
        )
        client.login()
        logger.info("登录成功，会话有效期至：%s", client.session_expiry)
        yield
    finally:
        # 清理资源
        if client:
            client.logout()
            logger.info("已释放登录会话")

app = FastAPI(lifespan=lifespan)

def validate_uri(uri: str) -> dict:
    """增强型参数校验"""
    if uri.count("|") < 2:
        raise ValueError("URI 格式错误")
    
    parts = uri.split("|")
    return {
        "FileName": parts[0],
        "Size": int(parts[1]),
        "Etag": parts[2].split("?")[0].lower(),
        "S3KeyFlag": parts[2].split("?")[1] if "?" in parts[2] else ""
    }

@app.get("/{uri:path}")
async def get_direct_link(request: Request, uri: str):
    global client
    try:
        logger.debug("请求参数: %s", uri)
        
        # 参数校验
        payload = validate_uri(uri)
        
        # 会话保活检查
        if client.needs_refresh():  # 假设 SDK 提供会话状态检查
            logger.info("会话续期中...")
            client.refresh()
        
        # 获取下载链接
        resp = check_response(client.download_info(payload))
        download_url = resp["data"]["DownloadUrl"]
        
        logger.info("生成直链: %s", download_url)
        return RedirectResponse(download_url, status_code=302)
    
    except ValueError as e:
        return JSONResponse({"error": str(e)}, 400)
    except Exception as e:
        logger.error("处理失败: %s", str(e), exc_info=True)
        return JSONResponse({"error": "内部错误"}, 500)
