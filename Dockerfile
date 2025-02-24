# 使用官方Python基础镜像，确保版本大于3.12
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录下的所有文件到工作目录
COPY . /app

# 安装依赖包
# 注意：这里需要根据你的script.py中实际使用的库来安装依赖
# 由于你的脚本中使用了多个第三方库，这里列出了一些可能的依赖，但可能不完整
# 你需要运行脚本并查看报错信息来补充所有缺失的依赖
RUN pip install --no-cache-dir \
    cachedict \
    orjson \
    p123client \
    wsgidav \

# 暴露端口
EXPOSE 8123

# 指定容器启动时执行的命令（这里假设你想运行这个脚本）
CMD ["python", "p123dav.py"]
