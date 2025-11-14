# 运行脚本说明 / Run Scripts Guide

本目录包含快速启动班级管理应用的脚本。

## 使用方法 / Usage

### Windows

双击运行或在命令行中执行：
```cmd
run_app.bat
```

### Linux/Mac

在终端中执行：
```bash
bash run_app.sh
# 或
chmod +x run_app.sh
./run_app.sh
```

### 从项目根目录运行

```bash
# Windows
scripts\run\run_app.bat

# Linux/Mac
bash scripts/run/run_app.sh
```

## 脚本说明 / Script Description

- **run_app.bat**：Windows批处理脚本，自动激活Python环境并运行应用
- **run_app.sh**：Linux/Mac Shell脚本，自动激活Python环境并运行应用

## 前置要求 / Prerequisites

1. 已安装Python 3.7+
2. 已安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```

## 默认登录信息 / Default Login

- 账号：`xigua`
- 密码：`123456`

## 问题排查 / Troubleshooting

### 找不到Python命令
确保Python已安装并添加到系统PATH：
```bash
python3 --version
# 或
python --version
```

### 缺少依赖包
安装所需依赖：
```bash
pip install -r requirements.txt
```

### 权限问题（Linux/Mac）
添加执行权限：
```bash
chmod +x run_app.sh
```
