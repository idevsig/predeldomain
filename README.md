# 预删除域名获取

`.cn`, `.top` 预删除的域名获取。


<a href="https://pypi.org/project/predeldomain" target="_blank">
    <img src="https://img.shields.io/pypi/v/predeldomain.svg" alt="Package version">
</a>

<a href="https://pypi.org/project/predeldomain" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/predeldomain.svg" alt="Supported Python versions">
</a>

---


## 使用方法
### 1. 安装依赖包：
- 方式一：通过 pypi
```bash
pip install predeldomain
```
- 方式二：通过代码仓库
```bash
pip install git+https://framagit.org/idev/predeldomain.git
```
- 方式三：通过本地仓库
```bash
pip install -e .
```
- 方式四：通过 wheel 包
```bash
pip install predeldomain-X.X.X-py3-none-any.whl
```

- 方式五：**Docker**

> **版本：** `latest`, `main`, <`TAG`>

| Registry                                                                                        | Image
|---------------------------------------------------------------------------------------------------|----------------------------
| [**Docker Hub**](https://hub.docker.com/r/idevsig/predeldomain)                                           | `idevsig/predeldomain`
| [**GitHub Container Registry**](https://github.com/idevsig/predeldomain/pkgs/container/predeldomain)            | `ghcr.io/idevsig/predeldomain`
| **Tencent Cloud Container Registry** | `ccr.ccs.tencentyun.com/idevsig/predeldomain`
| **Aliyun Container Registry** | `registry.cn-guangzhou.aliyuncs.com/idevsig/predeldomain`

### 2. 使用帮助

```bash
» predeldomain --help
usage: predeldomain [-h] [-d [1-30]] [-l [1-10]] [-m {1,2,3}] [-o OUPUT] [-s {cn,top}] [-t {text,json}] [-w WHOIS] [-v]

The domain to be pre-deleted.

options:
  -h, --help            show this help message and exit
  -d [1-30], --delay [1-30]
                        Delay: 1s to 30s
  -l [1-10], --length [1-10]
                        Length: 1 to 10
  -m {1,2,3}, --mode {1,2,3}
                        Mode: 1. Alphanumeric, 2. Numeric, 3. Alphabetic
  -o OUPUT, --ouput OUPUT
                        Output: print data to stdout
  -s {cn,top}, --suffix {cn,top}
                        Suffix: 'cn' or 'top'
  -t {text,json}, --type {text,json}
                        Save type: 'text' or 'json'
  -w WHOIS, --whois WHOIS
                        Whois: whois, qcloud, nic, westxyz, zzidc <NULL>
  -v, --version         Print version
```
1. length: 长度，不含后缀
2. mode: 模式， 1. 数字 + 字母, 2. 数字, 3. 字母
3. suffix: 域名后缀， 'cn' 或者 'top'
4. type: 保存类型， 'text' 或者 'json' （数据保存和发送通知的格式）
5. whois: whois, isp，查询可用的方式。
   > `留空`，则不查询，而是直接根据官网提供的数据判断；\
   > `whois`，则使用 `whois` 库查询；\
   > `qcloud` 则使用腾讯云（`qcloud.com`）的 API 查询；\
   > `westxyz` 则使用西部数码（`west.xyz`）的 API 查询；\
   > `westxyz` 则使用景安网络（`zzidc.com`）的 API 查询；\
   > `nic` 则使用官方注册局接口查询（当前仅支持 `top`）。
6. version: 版本信息
7. delay: 接口查询延时，单位秒，默认为 3。
8. ouput: 是否输出到控制台，默认为 `False`。

> 结果将会通过 PUSH 通知，和保存到本地文件。\
> 数据拆分为 `早期`、`今日`、`明日`、`后期`。`PUSH` 通知只发送今日和明日的数据。`log` text 日志方式则拆成三个文件 *早期*(`_prev.log`)、*今日*、明日及后期(`_next.log`)。json 日志方式则保存为 `_json.log`，以数组形式组合再转为 `JSON` 日志。\
> 可使用代理（解决 GitHub 获取域名列表缓慢的问题）。\

### 3. PUSH 通知
当前仅支持 [**Lark**](https://www.larksuite.com/) 以及 [**PushDeer**](http://www.pushdeer.com/)。依赖 [**ipush 库**](https://framagit.org/idev/pypush)，其它渠道可自行添加。

需要设置环境变量
```bash
# Lark
export LARK_TOKEN=""
export LARK_SECRET=""

# PushDeer
export PUSHDEER_TOKEN=""
```

## 开发

### 1. 前置开发环境

1. 使用 [**Rye**](https://rye.astral.sh/) 作为包管理工具

### 2. 开发流程

1. 安装依赖包：

```bash
# 同步
rye sync
```

2. 代码检测与格式化：

```bash
# 检测
rye run check

# 格式化
rye run format
```

3. 单元测试：

```bash
# rye test
rye run tests

# pytest
python -m pytest

# 打印测试报告
python -m pytest -s
```

### Docker Buildx Bake
```bash
docker buildx bake --print
docker buildx bake --print dev
```

## 仓库镜像

- https://git.jetsung.com/idev/predeldomain
- https://framagit.org/idev/predeldomain
- https://gitcode.com/idev/predeldomain
- https://github.com/idevsig/predeldomain
