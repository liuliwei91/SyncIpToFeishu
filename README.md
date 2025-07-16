# SyncIpToFeishu

绝对免费、连接质量最高的远程桌面工具自动同步本机IPv6地址到飞书文档的项目，通过云文档随时获取ipv6地址，可以通过ipv6访问远程桌面，或者访问其他的一些服务。

## 功能描述

- 定时获取本机IPv6地址
- 将IP地址和时间戳同步到指定的飞书文档
- 当IP地址变化时自动更新文档

## 依赖要求

- 必须拥有ipv6地址，包括本地和远程端设备
- Python 3.6+
- 依赖包：`requests` (通过`requirements.txt`安装)
- 注册飞书企业测试账号，创建测试应用，创建云文档，将测试应用添加为云文档的协作者，登录：https://open.feishu.cn/,获取app_id、app_secret，通过权限管理开通相关权限，通过api创建云文档的块，详情查看https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/guide#de57678b,可以通过右上角的“API调试台”进行api测试

## 安装与配置

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 复制`config.ini.example`为`config.ini`并填写配置：
```ini
[Feishu]
app_id = your_app_id
app_secret = your_app_secret
auth_url = https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal
docx_url = your_docx_url

[Settings]
get_ipv6_url = http://6.ipw.cn
log_file = syncip.log
```

## 使用方法

- Windows: 双击`start.bat`
- Linux: 运行`start.sh`

## 开机自启动

- Windows: 将`start.bat`添加到开机启动，win+R输入`shell:startup`回车，将`start.bat`复制到该目录，需要将脚本的路径修改为绝对路径
- Linux: 将`start.sh`添加到开机启动，推荐使用`crontab`添加定时任务

## 日志查看

日志会输出到`syncip.log`文件，也会在控制台显示

## 注意事项

- 请确保网络连接正常
- 飞书应用需要有文档编辑权限
- 程序会每5分钟检查一次IP变化，可以自行设置间隔，频率太高会被http://6.ipw.cn拦截
