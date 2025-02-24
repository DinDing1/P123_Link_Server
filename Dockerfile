# 使用官方Python基础镜像，确保版本大于3.12
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录下的所有文件到工作目录
COPY . /app

RUN pip install --no-cache-dir cachedict orjson wsgidav p123client

# 暴露端口
EXPOSE 8123

# 指定容器启动时执行的命令（这里假设你想运行这个脚本）
CMD ["python", "p123dav.py"]
