FROM python:3.12-slim

WORKDIR /app

# 仅安装必要的编译工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY p123dav.py .

# 安装依赖（不再需要Git）
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8123

CMD ["python", "p123dav.py"]
