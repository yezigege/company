from tasks import celery_app
from log_config import logger_celery

import smtplib
from email.mime.text import MIMEText
from email.header import Header


@celery_app.task()
def celery_task_test():
    logger_celery.info(f"开始运行......")
    
    # 第三方 SMTP 服务
    mail_host="smtp.163.com"  #设置服务器
    mail_user="xxx@163.com"    #用户名
    mail_pass="ERULBYZZSFUIVAQCF"   #口令 
    
    
    sender = 'xxx@163.com'
    receivers = ['xxx@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    
    message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
    message['From'] = Header("流体网络", 'utf-8')
    message['To'] =  Header("测试", 'utf-8')
    
    subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(subject, 'utf-8')
    
    
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        logger_celery.info("邮件发送成功")
    except smtplib.SMTPException as e:
        logger_celery.info(f"Error: 无法发送邮件, err_info: {str(e)}")
    
    return [i for i in range(10)]