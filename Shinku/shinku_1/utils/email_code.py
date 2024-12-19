import random

from django.core.mail import send_mail


def send_code(to_email,email_code):
    """
    发送邮箱验证码
    :param to_email: 发到这个邮箱
    :return: 成功：0 失败 -1
    """
    # 生成邮箱验证码

    EMAIL_FROM = "1778469207@qq.com"  # 邮箱来自
    email_title = '邮箱激活'
    email_body = "您的邮箱注册验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(email_code)

    try:
        send_mail(email_title, email_body, EMAIL_FROM, [to_email])
    except Exception as e:

        # 邮件发送失败，返回错误信息
        return 0
    return 1
