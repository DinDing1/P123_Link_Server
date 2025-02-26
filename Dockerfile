# 使用完整镜像确保依赖可用性
FROM python:3.12

WORKDIR /app
COPY . .

# 安装系统依赖（修正续行符）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libffi-dev \
    rustc \
    cargo \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
RUN pip install --no-cache-dir -U \
    python-123-client \
    orjson \
    httpx \
    wsgidav \
    cachedict \
    property \
    sqlitetools \
    tenacity

EXPOSE 8123
CMD ["python", "p123dav.py"]