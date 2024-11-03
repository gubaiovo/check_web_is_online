import smtplib
import requests
from time import sleep
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime



def send_email(receiver, url, time):
    
    # 设置发件人和收件人信息
    sender_email = "470014599@qq.com"
    password = "kqaphslgcwgzbjac"  # QQ 邮箱授权码

    # 创建邮件对象
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver
    message["Subject"] = "网站上线"

    # 邮件正文
    body = f"网站已经上线 {url}，当前时间: {time}"
    message.attach(MIMEText(body, "plain"))

    # 连接到 SMTP 服务器并发送邮件
    try:
        # 连接到 QQ 邮箱的 SMTP 服务器
        server = smtplib.SMTP("smtp.qq.com", 587)
        server.starttls()  # 启用 TLS 加密
        server.login(sender_email, password)  # 登录 SMTP 服务器

        # 发送邮件
        server.sendmail(sender_email, receiver, message.as_string())
        print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败: {e}")
    finally:
        server.quit()  # 关闭连接



def checkweb(receiver, url):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"网站正常 {url}，当前时间: {current_time}")
            send_email(receiver, url, current_time)
        else:
            print(f"网站异常{response.status_code}, 但是网站在线 {url}，当前时间: {current_time}")
            send_email(receiver, url, current_time)
    except Exception as e:
        print(f"网站异常! {e}，当前时间: {current_time}")

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None
def is_valid_url(url):
    pattern = r'^(http|https)://[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    return re.match(pattern, url) is not None

print(r"""
  ________        __________        .__ 
 /  _____/ __ __  \______   \_____  |__|
/   \  ___|  |  \  |    |  _/\__  \ |  |
\    \_\  \  |  /  |    |   \ / __ \|  |
 \______  /____/   |______  /(____  /__|
        \/                \/      \/    
""")
print("ctrl + c 退出程序")
time = int(input("请输入检测间隔时间(秒): "))
receiver = input("请输入收件人邮箱: ")
while not is_valid_email(receiver):
    print("邮箱格式不正确，请重新输入。")
    receiver = input("请输入收件人邮箱: ")
url = input("请输入网站地址(http/https不可省略): [ https(http)://www.example.com ]: ")
while not is_valid_url(url):
    print("网站地址格式不正确，请重新输入。")
    url = input("请输入网站地址(http/https不可省略): [ https(http)://www.example.com ]: ")
while True:
    checkweb(receiver, url)
    sleep(time)