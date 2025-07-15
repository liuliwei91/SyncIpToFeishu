import time
import logging
import configparser
import json
import requests
import os

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
# 读取配置文件
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

APP_ID = config.get('Feishu', 'app_id', fallback='')
APP_SECRET = config.get('Feishu', 'app_secret', fallback='')
AUTH_URL = config.get('Feishu', 'auth_url', fallback="")
DOCX_URL = config.get('Feishu', 'docx_url', fallback="")
GET_IPV6_URL = config.get('Settings', 'get_ipv6_url', fallback="")


# 日志配置
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), config.get('Settings', 'log_file', fallback='syncip.log'))
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(LOG_FILE, encoding='utf-8'),
                        logging.StreamHandler()
                    ])

#获取ipv6地址
def get_ipv6_address():
    url = GET_IPV6_URL
    try:
        res = requests.get(url, timeout=5)  # 设置超时时间为5秒
        logging.info(f'当前ipv6地址为：{res.text}')
        return res.text
    except requests.Timeout:
        logging.warning('请求超时，重试中...')
        time.sleep(5)
        return get_ipv6_address()  # 重试
    except Exception as e:
        logging.error(f"An error occurred: {e}")

#获取飞书token
def get_auth_token():
    auth_payload = json.dumps({
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    })

    auth_headers = {
    'Content-Type': 'application/json'
    }
    try:
        auth_res = requests.request("POST", AUTH_URL, headers=auth_headers, data=auth_payload, timeout=5)
        auth_res_json = auth_res.json()
        auth_token = auth_res_json["tenant_access_token"]
        logging.info(f'当前tenant_access_token为：{auth_token}')
        return auth_token
    except requests.Timeout:
        logging.warning('请求超时，重试中...')
        time.sleep(5)
        return get_auth_token()  # 重试
    except Exception as e:
        logging.error(f"An error occurred: {e}")

#将ip写入到飞书文档
def update_feishu_docx(auth_token, current_time, ip_now):
    payload = json.dumps({
            "children": [
                {
                    "block_type": 2,
                    "text": {
                        "elements": [
                            {
                                "text_run": {
                                    "content": current_time
                                }
                            }
                        ],
                        "style": {}
                    }
                },
                {
                    "block_type": 2,
                    "text": {
                        "elements": [
                            {
                                "text_run": {
                                    "content": ip_now
                                }
                            }
                        ],
                        "style": {}
                    }
                }
            ],
            "index": 0
        })

    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {auth_token}'
    }

    try:
        response = requests.request("POST", DOCX_URL, headers=headers, data=payload)    
        logging.info(response.text)
    except Exception as e:
        logging.error(f"An error occurred: {e}")



ip=''
while True:
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    logging.info(f'当前时间为：{current_time}')

    auth_token=get_auth_token()
    ip_now=get_ipv6_address()

    if ip_now!=ip:
        ip=ip_now
        logging.info('发生变化，开始同步')
        update_feishu_docx(auth_token, current_time, ip_now)
    else:
        logging.info('未发生变化，不需同步')    
    
    time.sleep(300)  # 5分钟执行一次