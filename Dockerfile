FROM python:3.12-slim

WORKDIR /app

# 安装编译依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制文件到容器
COPY requirements.txt p123dav.py ./

# 设置文件权限
RUN chmod +x p123dav.py

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8123

# 启动命令
CMD ["python", "/app/p123dav.py"]
