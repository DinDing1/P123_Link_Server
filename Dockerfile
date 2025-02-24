# 使用 Alpine 镜像作为基础
FROM python:3.13.2-alpine

# 設置工作目錄
WORKDIR /app

# 安裝系統依賴（可根據需要調整）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴列表並安裝Python依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製腳本文件
COPY p123dav(1).py ./p123dav.py

# 設置環境變量（默認值可選）
ENV P123_PASSPORT=""
ENV P123_PASSWORD=""
ENV PORT=8123

# 暴露端口
EXPOSE $PORT

# 運行命令
CMD ["python", "p123dav.py"]
