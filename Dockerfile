# 使用 Alpine 镜像作为基础
FROM python:3.13.2-alpine

# 安装系统依赖
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev

# 其他部分保持不变
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY p123dav.py ./p123dav.py

# 设置环境变量
ENV PORT=8123

# 暴露端口
EXPOSE $PORT

# 运行命令
CMD ["python", "p123dav.py"]
