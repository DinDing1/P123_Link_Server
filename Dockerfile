# 使用官方 Python 基础镜像
FROM python:3.12-slim

# 安装必要的系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制依赖列表
COPY requirements.txt .

# 安装 Python 依赖（包含 python-123-client）
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY main.py .

# 暴露服务端口
EXPOSE 8123

# 通过环境变量注入认证信息
ENV P123_PASSPORT="your_passport" \
    P123_PASSWORD="your_password"

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8123"]