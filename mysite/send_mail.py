import os
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

if __name__ == '__main__':
    # send_mail(
    #     '测试邮件',
    #     '邮件验证',
    #     '15530258872@163.com',
    #     ['1685715822@qq.com']
    # )
    # 某些邮件公司可能不开放smtp服务
    # 某些公司要求使用ssl安全机制
    # 某些smtp服务对主机名格式有要求
    subject,from_email,to = '测试邮件','15530258872@163.com','1685715822@qq.com'
    text_content = '欢迎'
    html_content = '<p>欢迎访问<a href="www.aichunhui.cn" target="_blank">艾春辉的主页</a></p>'
    msg = EmailMultiAlternatives(subject,text_content,from_email,[to])
    msg.attach_alternative(html_content,"text/html")
    msg.send()