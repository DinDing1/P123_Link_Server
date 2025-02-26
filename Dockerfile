# 使用官方 Python 镜像作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY . .

# 安装系统依赖（如有需要）
# RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev

# 安装 Python 依赖
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir \
    orjson \
    httpx \
    wsgidav \
    cachedict \
    property \
    sqlitetools3 \
    tenacity

# 暴露 WebDAV 服务端口
EXPOSE 8123

# 设置启动命令
CMD ["python", "p123dav.py"]
