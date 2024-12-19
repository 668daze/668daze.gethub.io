"""
URL configuration for Shinku project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shinku_1.views.admin import goods, main_type, users, user_group,order
from shinku_1.views.users import base, register
from shinku_1.views import login
from web_celery.sms import tasks

urlpatterns = [
    path("admin/", admin.site.urls),
    path('index1/', base.index1),
    path('index2/', base.index2),
    path('index3/', base.index3),
    path('index4/', base.index4),

    path('login/register/email/', register.register_email),
    path('login/register/', register.register_info),
    path('login/register/', register.register_info),


    path('login/register/send_mail_<str:to_email>', tasks.send_sms),
    path('login/', login.login),
    path('logout/', login.logout),
    path('image/captcha_code/', login.captcha),

    # 商品管理
    path("admin_goods", goods.goods_list),
    path("admin_goods/add", goods.goods_add),
    path('admin_goods/<int:uid>/delete/', goods.goods_delete),
    path('admin_goods/<int:uid>/edit/', goods.goods_edit),

    # 商品分类管理
    path("admin_mainType", main_type.maintype_list),
    path("admin_mainType/add/", main_type.maintype_list_add),
    path('admin_mainType/<int:uid>/delete/', main_type.maintype_list_delete),
    path('admin_mainType/<int:uid>/edit/', main_type.maintype_list_edit),

    # 用户管理
    path("admin_users", users.users_list),
    path("admin_users/add", users.users_add),
    path('admin_users/<int:uid>/delete/', users.users_delete),
    path('admin_users/<int:uid>/edit/', users.users_edit),

    # 用户组管理
    path("admin_userGroup", user_group.user_group_list),
    path("admin_userGroup/add/", user_group.user_group_list_add),
    path('admin_userGroup/<int:uid>/delete/', user_group.user_group_list_delete),
    path('admin_userGroup/<int:uid>/edit/', user_group.user_group_list_edit),

    #订单管理
    path("admin_order", order.order_list),
    path("admin_order/add/",order.order_list_add),
    path('admin_order/<int:uid>/delete/', order.order_list_delete),
    path('admin_order/<int:uid>/edit/', order.order_list_edit),
]
