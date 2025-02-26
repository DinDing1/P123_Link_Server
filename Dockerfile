# 使用官方 Python 镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 复制代码到容器
COPY . .

# 安装系统编译依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \                         # C 编译器
    python3-dev \                 # Python 开发头文件
    libffi-dev \                  # libffi 库（部分加密包需要）
    rustc \                       # Rust 编译器（orjson 等包需要）
    cargo \                       # Rust 包管理工具
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖（不固定版本）
RUN pip install --no-cache-dir -U \
    python-123-client \           # 123 云盘客户端库
    orjson \                      # 高性能 JSON 解析库
    httpx \                       # 异步 HTTP 客户端
    wsgidav \                     # WebDAV 服务器框架
    cachedict \                   # 缓存字典库
    property \                    # 属性管理库
    sqlitetools \                 # SQLite 工具库
    tenacity                     # 重试机制库

# 暴露 WebDAV 服务端口
EXPOSE 8123

# 启动命令
CMD ["python", "p123dav.py"]