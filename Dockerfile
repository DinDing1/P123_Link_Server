# 使用官方的 Python 3.9 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录下的所有文件到容器的 /app 目录
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir fastapi uvicorn

# 克隆 p123 源码
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/ChenyangGao/web-mount-packs.git /app/web-mount-packs

# 将 p123 模块添加到 Python 路径
ENV PYTHONPATH "${PYTHONPATH}:/app/web-mount-packs"

# 暴露端口
EXPOSE 8123

# 运行应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8123"]
