from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse, JSONResponse
from p123 import P123Client, check_response
from contextlib import asynccontextmanager
import logging
import os
import urllib.parse

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
    """修复版生命周期管理"""
    global client
    try:
        client = P123Client(
            passport=os.getenv("P123_PASSPORT"),
            password=os.getenv("P123_PASSWORD")
        )
        # 仅登录一次且无重试
        client.login()
        logger.info("客户端初始化完成")
        yield
    except Exception as e:
        logger.critical(f"启动失败: {str(e)}")
        raise
    finally:
        client = None

app = FastAPI(lifespan=lifespan)

def validate_uri(uri: str) -> dict:
    """增强型参数解析"""
    try:
        # URL 解码
        decoded_uri = urllib.parse.unquote(uri)
        
        # 分割主要部分和查询参数
        main_part, _, query = decoded_uri.partition("?")
        parts = main_part.split("|")
        
        if len(parts) < 3:
            raise ValueError("URI 必须包含文件名|大小|etag 三部分")
            
        # 解析查询参数
        query_params = {}
        for param in query.split("&"):
            if "=" in param:
                key, value = param.split("=", 1)
                query_params[key.strip().lower()] = value.strip()
        
        return {
            "FileName": parts[0],
            "Size": int(parts[1]),
            "Etag": parts[2],
            "S3KeyFlag": query_params.get("s3keyflag", "")
        }
    except ValueError as e:
        raise
    except Exception as e:
        raise ValueError(f"参数解析失败: {str(e)}")

@app.get("/{uri:path}")
async def generate_link(request: Request, uri: str):
    global client
    try:
        # 参数处理
        payload = validate_uri(uri)
        logger.debug(f"请求参数: {payload}")
        
        if not payload["S3KeyFlag"]:
            raise ValueError("缺少必需参数 s3keyflag")
        
        # 获取下载链接
        resp = check_response(client.download_info(payload))
        return RedirectResponse(resp["data"]["DownloadUrl"])
        
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"处理失败: {str(e)}", exc_info=True)
        return JSONResponse(
            {"error": "内部服务错误"}, 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
