import random
from distutils.command.register import register
from random import randint

from Demos.win32ts_logoff_disconnected import session

from shinku_1.utils.Forms import UsersModelForm
from django.shortcuts import render, redirect
from shinku_1 import models
from django import forms


class Form(UsersModelForm):
    captcha = forms.CharField(
        label="验证码",
        widget=forms.TextInput(attrs={'class': ' form-control form-captcha'}),
        required=True,
    )
    model = models.UserInfo

    fields = ["username", "password", "confirm_password", "email", 'captcha']



from shinku_1.utils.email_code import send_code
from django.http import JsonResponse


def register_email(request):
    """AJAX发送邮箱验证码"""

    str_email = request.POST.get('email')
    if str_email == "":
        return JsonResponse({'status': False, 'error': "请填写邮箱。"})
    email_code = random.randint(1000, 9999)
    if send_code(str_email, email_code):
        # 发送之后再写到session
        request.session['register'] = {'email_code': email_code}
        request.session.set_expiry(2*60)
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': "请确认邮箱正确后重试。"})


def register_info(request):
    """注册"""
    # 通过链接访问页面
    if request.method == 'GET':
        form = Form()
        return render(request, "HTML/users/register.html", {'form': form})
    # IF POST\提交表单
    form = Form(data=request.POST)
    if form.is_valid():
        # 邮箱校验
        captcha_code = form.cleaned_data.pop('captcha')
        input_code = request.session.get('register')
        if input_code is None:
            form.add_error('email', "你还未发送邮件,或者已过期")
            return render(request, "HTML/users/register.html", {'form': form})

        print(input_code.get('email_code'),captcha_code)
        if str(input_code.get('email_code')) != captcha_code:
            form.add_error('captcha', "验证码错误")
            return render(request, "HTML/users/register.html", {'form': form})

        form.save()
        request.session.clear()
        return redirect('/login/')
    # 输入错误
    print(form.errors)
    return render(request, "HTML/users/register.html", {'form': form})
