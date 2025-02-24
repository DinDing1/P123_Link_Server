# 使用 Python 官方镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 升级 pip
RUN pip install --upgrade pip

# 复制依赖列表并安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制主脚本
COPY p123dav.py /app/p123dav.py

# 设置环境变量
ENV PORT=8123

# 暴露端口
EXPOSE $PORT

# 运行命令
CMD ["python", "/app/p123dav.py"]
