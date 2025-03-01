from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from p123 import P123Client, check_response
from contextlib import asynccontextmanager
import logging
import os

# 日志配置
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# 全局客户端实例
client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理 (修复版)"""
    global client
    try:
        # 仅使用必要参数初始化
        client = P123Client(
            passport=os.getenv("P123_PASSPORT"),
            password=os.getenv("P123_PASSWORD")
        )
        client.login()
        logger.info("登录成功")
        yield
    except Exception as e:
        logger.critical(f"初始化失败: {str(e)}")
        raise
    finally:
        client = None

app = FastAPI(lifespan=lifespan)

def validate_uri(uri: str) -> dict:
    """安全的参数校验"""
    parts = uri.split("|")
    if len(parts) < 3:
        raise ValueError("URI 必须包含 | 分隔的三部分")
    return {
        "FileName": parts[0],
        "Size": int(parts[1]),
        "Etag": parts[2].split("?")[0],
        "S3KeyFlag": parts[2].split("?")[1] if "?" in parts[2] else ""
    }

@app.get("/{uri:path}")
async def get_link(request: Request, uri: str):
    global client
    try:
        # 基础校验
        payload = validate_uri(uri)
        
        # 获取下载链接
        resp = check_response(client.download_info(payload))
        return RedirectResponse(resp["data"]["DownloadUrl"])
    
    except ValueError as e:
        return JSONResponse({"error": str(e)}, 400)
    except Exception as e:
        logger.error(f"处理失败: {str(e)}")
        return JSONResponse({"error": "内部错误"}, 500)
