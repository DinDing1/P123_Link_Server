# 使用 Python 3.12 的官方鏡像
FROM python:3.12-slim

# 設置工作目錄
WORKDIR /app

# 安裝系統依賴（部分Python包需要編譯工具）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 複製項目文件
COPY requirements.txt .
COPY p123dav.py .

# 安裝Python依賴
RUN pip install --no-cache-dir -r requirements.txt

# 設置環境變量（密碼建議通過運行時傳入）
ENV P123_PASSPORT=""
ENV P123_PASSWORD=""

# 暴露端口
EXPOSE 8123

# 啟動命令
CMD ["python", "p123dav.py"]
