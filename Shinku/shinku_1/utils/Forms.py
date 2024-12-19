import random
from os.path import exists

from django import forms
from shinku_1 import models
from django.core.exceptions import ValidationError
from shinku_1.utils.encrypt import md5


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = models.Order

        # 不要用字典，或者集合，因为那是哈希表显示顺序会乱
        fields = ["seller", "buyer", "status"]

        widgets = {
            "seller": forms.TextInput(attrs={'class': 'form-control', 'placeholder': '卖家'}),
            "buyer": forms.TextInput(attrs={'class': 'form-control', 'placeholder': '买家'}),
            "status": forms.Select(attrs={'class': 'form-control', 'placeholder': '状态'}),
        }


class GoodsModelForm(forms.ModelForm):
    class Meta:
        model = models.Goods

        # 不要用字典，或者集合，因为那是哈希表显示顺序会乱
        fields = ["name", "owner", "price", "description", 'main_type', 'status']

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            "owner": forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ownerID'}),
            "price": forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            "description": forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            "main_type": forms.Select(attrs={'class': 'form-control', 'placeholder': 'Main Type'}),
            "status": forms.Select(attrs={'class': 'form-control', 'placeholder': 'Status'}),
        }


class MainTypeModelForm(forms.ModelForm):
    class Meta:
        model = models.MainType
        # 不要用字典，或者集合，因为那是哈希表显示顺序会乱
        fields = ["name"]

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
        }


class AdminUsersModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo

        # fields = ["username", "password", "confirm_password", "email",]
        fields = ["username", "email", 'user_group', 'status']
        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            "email": forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            "user_group": forms.Select(attrs={'class': 'form-control', 'placeholder': 'user_group'}),
            "status": forms.Select(attrs={'class': 'form-control', 'placeholder': 'Status'}),
        }


class AdminUsersModelForm2(forms.ModelForm):
    class Meta:
        model = models.UserInfo

        # fields = ["username", "password", "confirm_password", "email",]
        fields = ["username", "password", "email", 'user_group', 'status']
        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            "password": forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            "email": forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            "user_group": forms.Select(attrs={'class': 'form-control', 'placeholder': 'user_group'}),
            "status": forms.Select(attrs={'class': 'form-control', 'placeholder': 'Status'}),
        }

    def clean_password(self):
        # 加密
        pwd = self.cleaned_data.get("password")
        md5_password = md5(pwd)
        return md5_password


class UsersModelForm(forms.ModelForm):
    confirm_password = forms.CharField(label="确认密码",
                                       widget=forms.PasswordInput(attrs={
                                           'class': 'form-control',
                                           'placeholder': 'Confirm Password',
                                       }))

    class Meta:
        model = models.UserInfo

        # fields = ["username", "password", "confirm_password", "email",]
        fields = ["username", "password", "confirm_password", "email", 'user_group']
        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            "password": forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            "email": forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            "user_group": forms.Select(attrs={'class': 'form-control', 'placeholder': 'user_group'}),

        }

    def clean_confirm_password(self):
        confirm = self.cleaned_data.get("confirm_password")
        confirm = md5(confirm)
        password = self.cleaned_data.get("password")
        if confirm != password:
            raise ValidationError("密码不一致")
        # return 保存的该字段的值
        return confirm

    def clean_password(self):

        # 加密
        pwd = self.cleaned_data.get("password")
        md5_password = md5(pwd)

        # 重置密码用，检验是否和原密码一直
        exists = models.UserInfo.objects.filter(id=self.instance.pk, password=md5_password).exists()
        if exists:
            raise ValidationError("不能和原密码一致")
        return md5_password


class UserGroupModelForm(forms.ModelForm):
    class Meta:
        model = models.UserGroup
        # 不要用字典，或者集合，因为那是哈希表显示顺序会乱
        fields = ["name"]

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
        }
