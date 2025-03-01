version: '3.8'
services:
  p123link:
    image: dinding1/p123link:latest
    container_name: p123link
    network_mode: host
    environment:
      - P123_PASSPORT=123账号
      - P123_PASSWORD=123密码
    restart: always
