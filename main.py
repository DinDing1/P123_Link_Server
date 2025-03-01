from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from p123 import P123Client, check_response

# TODO: 改成你自己的账户和密码
client = P123Client(passport="13554540004", password="ztj040712")

app = FastAPI(debug=True)

@app.get("/{uri:path}")
@app.head("/{uri:path}")
async def index(request: Request, uri: str):
    try:
        # 解析 URI（格式：文件名|大小|etag）
        if uri.count("|") < 2:
            return JSONResponse({"state": False, "message": "URI 格式错误，应为 '文件名|大小|etag'"}, 400)
        
        # 提取参数
        parts = uri.split("|")
        file_name = parts[0]
        size = parts[1]
        etag = parts[2].split("?")[0]  # 提取 etag（忽略查询参数部分）
        
        # 提取 s3keyflag（从查询参数）
        s3_key_flag = request.query_params.get("s3keyflag", "")  # 关键修改
        
        # 构造下载参数
        payload = {
            "FileName": file_name,
            "Size": int(size),
            "Etag": etag,
            "S3KeyFlag": s3_key_flag  # 参数名需与 API 一致（注意大小写）
        }
        
        # 获取下载链接
        download_resp = check_response(client.download_info(payload))
        download_url = download_resp["data"]["DownloadUrl"]
        return RedirectResponse(download_url, 302)
    
    except Exception as e:
        return JSONResponse({"state": False, "message": f"内部错误: {str(e)}"}, 500)

if __name__ == "__main__":
    from uvicorn import run
    run(app, host="0.0.0.0", port=8123)