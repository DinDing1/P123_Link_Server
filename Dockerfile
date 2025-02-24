# Dockerfile
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
RUN pip install --no-cache-dir \
    p123api \
    cachedict \
    wsgidav \
    cheroot \
    orjson \
    sqlitetools3

# 复制应用代码
COPY p123dav.py .

# 创建数据目录并设置权限
RUN mkdir /data && chmod 777 /data

# 声明数据卷
VOLUME /data

# 暴露端口
EXPOSE 8123

# 启动命令
CMD ["python3", "p123dav.py"]
