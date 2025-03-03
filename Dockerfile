# 使用官方的 Python 3.9 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装 Git
RUN apt-get update && apt-get install -y git

# 复制 requirements.txt 到容器
COPY requirements.txt /app/

# 安装 Python 依赖
RUN pip install --no-cache-dir fastapi uvicorn requests
RUN pip install --no-cache-dir git+https://github.com/ChenyangGao/web-mount-packs.git#subdirectory=python-123-client

# 复制应用程序代码到容器
COPY . /app

# 暴露端口
EXPOSE 8123

# 运行应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8123"]
