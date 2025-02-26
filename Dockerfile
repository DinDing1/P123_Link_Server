# 第一阶段：构建依赖
FROM python:3.12 as builder
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y gcc python3-dev rustc cargo
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

# 第二阶段：生产镜像
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .
EXPOSE 8123
CMD ["python", "p123dav.py"]
