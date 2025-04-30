# Excel 右键上传工具菜单注册器

本工具用于将 Excel 文件（`.xlsx`）的右键菜单中添加一项“上传 Excel”，点击后自动调用指定程序（支持 `.py` 和 `.exe` 形式）执行上传操作。

## 📦 功能说明

- ✅ 支持在右键菜单中添加/移除上传命令
- ✅ 自动判断是开发环境（使用 `.py`）还是打包环境（使用 `.exe`）
- ✅ 安全操作注册表，仅对 `.xlsx` 文件生效
- ✅ 控制台交互式执行，无 GUI

## 🛠 文件说明

| 文件名                 | 说明                      |
|---------------------|-------------------------|
| `register_menu.py`  | 注册/注销 Excel 右键菜单的主程序    |
| `upload_excel.py`   | 实际执行上传的 Python 脚本（开发环境） |
| `register_menu.exe` | 打包后的注册工具（打包环境）          |
| `upload_excel.exe`  | 打包后的上传工具（打包环境）          |
| `config.ini`        | 配置文件                    |

## 🚀 使用方法

### 1. 注册右键菜单

```bash
python register_menu.py
# 必须管理员权限运行，否则报错
```
```bash
管理员权限运行 register_menu.exe
```
### 一、注意
两个文件必须放在同一文件夹内，必须先完成注册右键菜单，才能执行右键上传

### 二、关于配置文件
```ini
[server]
# 后端服务器IP
host = 172.16.2.50  
# 后端服务器port
port = 5001
# 超时时间(s)
timeout = 40
```


MIT License

Copyright (c) 2025 [PING-GAN]

