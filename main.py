import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from p123 import P123Client, check_response
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("direct_link_service.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# 从环境变量中读取账号和密码
PASSPORT = os.getenv("P123_PASSPORT")
PASSWORD = os.getenv("P123_PASSWORD")

if not PASSPORT or not PASSWORD:
    raise ValueError("请配置 P123_PASSPORT 和 P123_PASSWORD 环境变量")

# 初始化客户端并显式登录
client = P123Client(passport=PASSPORT, password=PASSWORD)
client.login()  # 关键修复：显式登录

app = FastAPI(debug=True)

@app.get("/{uri:path}")
@app.head("/{uri:path}")
async def index(request: Request, uri: str):
    try:
        logger.info(f"收到请求: {request.url}")
        
        # 解析 URI（格式：文件名|大小|etag）
        if uri.count("|") < 2:
            return JSONResponse({"state": False, "message": "URI 格式错误，应为 '文件名|大小|etag'"}, 400)
        
        parts = uri.split("|")
        file_name = parts[0]
        size = parts[1]
        etag = parts[2].split("?")[0]
        s3_key_flag = request.query_params.get("s3keyflag", "")
        
        # 构造字典参数（与原代码兼容）
        payload = {
            "FileName": file_name,
            "Size": int(size),
            "Etag": etag,
            "S3KeyFlag": s3_key_flag
        }
        
        # 使用原 download_info 方法
        download_resp = check_response(client.download_info(payload))
        download_url = download_resp["data"]["DownloadUrl"]
        logger.info(f"成功生成直链: {download_url}")
        return RedirectResponse(download_url, 302)
    
    except Exception as e:
        logger.error(f"处理失败: {str(e)}", exc_info=True)
        return JSONResponse({"state": False, "message": f"内部错误: {str(e)}"}, 500)

if __name__ == "__main__":
    from uvicorn import run
    run(app, host="0.0.0.0", port=8123)
