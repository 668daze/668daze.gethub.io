from os.path import exists

from Demos.win32ts_logoff_disconnected import session
from django import forms
from django.shortcuts import render, HttpResponse, redirect
from shinku_1.utils.encrypt import md5
from shinku_1 import models


class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={'class': 'form-control input_border'}),
        required=True,
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True, attrs={'class': 'form-control input_border'}),
        required=True,
    )
    captcha = forms.CharField(
        label="验证码",
        widget=forms.TextInput(attrs={'class': ' form-control input_border form-captcha'}),
        required=True,
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return md5(password)


def login(request):
    """get"""
    if request.method == 'GET':
        form = LoginForm()
        return render(request, "HTML/login.html", {'form': form})
    """post"""
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证码校验
        captcha_code = form.cleaned_data.pop('captcha')
        code = request.session.get('captcha_code', "")  # 可能为空

        code=captcha_code

        if code.upper() != captcha_code.upper():
            form.add_error('captcha', "验证码错误")
            return render(request, "HTML/login.html", {'form': form})
        # 密码校验
        user_object = models.UserInfo.objects.filter(**form.cleaned_data).first()
        if not user_object:
            # 密码错误
            form.add_error("password", "用户名或密码错误")
            return render(request, "HTML/login.html", {'form': form})
        # 密码正确
        # 生成随机字符串和用户信息写道cookie，session(Django自动吧随机字符串加进去了)
        request.session['info'] = {'id': user_object.id, 'name': user_object.username}
        # 设置过期时间
        request.session.set_expiry(60 * 60 * 24 * 3)
        # request.session.set_expiry(3)
        return redirect('/admin_goods')

    return render(request, "HTML/login.html", {'form': form})


def logout(request):
    """注销"""
    id=request.session['info']['id']
    request.session.clear()

    return redirect('/login/')


from io import BytesIO
from shinku_1.utils import captcha_code


def captcha(request):
    """"图片验证码"""
    img, code_str = captcha_code.code()
    request.session['captcha_code'] = code_str
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, format='JPEG')
    return HttpResponse(stream.getvalue(), content_type='image/jpeg')
