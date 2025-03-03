# 使用官方的 Python 3.9 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装 Git 和依赖项
RUN apt-get update && apt-get install -y git

# 克隆 web-mount-packs 仓库
RUN git clone https://github.com/ChenyangGao/web-mount-packs.git /app/web-mount-packs

# 复制当前目录下的所有文件到容器的 /app 目录
COPY . /app

# 安装 Python 依赖
RUN pip install --no-cache-dir fastapi uvicorn

# 将 web-mount-packs 目录添加到 PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/app/web-mount-packs"

# 暴露端口
EXPOSE 8123

# 运行应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8123"]
