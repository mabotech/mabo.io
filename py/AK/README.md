

# 说明

AK客户端轮询AK Server，将结果保存到Redis中。
 

## AK Client

数据采集客户端

配置文件 ak_client.toml


客户端打包

执行make

Makefile

单个文件（带图标）

pyinstaller --onefile --icon=app.ico ak_client.py 

# 打包环境的构建

- redis
- gevent
- influxdb (op)
- logbook
- toml
- mako
- pywin32 (python.exe Scripts\pywin32_postinstall.py -install)
- pyinstaller
- mabopy Singleton


## AK 指令




## AK Server模拟器

ak_server.py

配置文件 ak_server.toml

## 部署说明

拷贝到指定目录

日志文件


