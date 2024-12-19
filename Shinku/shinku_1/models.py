from django.db import models
from django.contrib.auth.models import Group

# Create your models here.
class MainType(models.Model):
    name = models.CharField(max_length=10, unique=True, verbose_name="主要总类")

    def __str__(self):
        """
            重写__str__方法，这样只要打印这个类的都会显示name字段
        """
        return f'{self.name}'





class UserGroup(models.Model):
    name = models.CharField(max_length=16, verbose_name="组名")
    def __str__(self):
        """
            重写__str__方法，这样只要打印这个类的都会显示name字段
        """
        return f'{self.name}'


class UserInfo(models.Model):
    username = models.CharField(max_length=16, verbose_name="用户名")
    password = models.CharField(max_length=32, verbose_name="密码")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    email = models.EmailField(verbose_name="邮箱")
    user_group = models.ForeignKey(UserGroup,on_delete=models.PROTECT,default=1,blank=True)

    status_choices = (
        (0, "封禁"),
        (1,"使用中"),
        (2,"已注销")
    )
    status=models.SmallIntegerField(choices=status_choices, default=1,verbose_name="状态")

    def __str__(self):
        """
            重写__str__方法，这样只要打印这个类的都会显示name字段
        """
        return f'{self.username}'



class Goods(models.Model):
    name = models.CharField(max_length=10, verbose_name="商品名称")
    owner=models.ForeignKey(UserInfo,on_delete=models.SET_DEFAULT,default=-1)
    price = models.DecimalField(max_digits=5, decimal_places=2,verbose_name="价格")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    description = models.CharField(max_length=100, verbose_name="商品描述")
    main_type = models.ForeignKey(MainType, on_delete=models.PROTECT)

    status_choices = (
        (0, "商品下架"),
        (1, "商品上架"),
        (2, "商品被ban"),
    )
    status = models.SmallIntegerField(choices=status_choices, default=1, verbose_name="状态")

    def __str__(self):
        """
            重写__str__方法，这样只要打印这个类的都会显示name字段
        """
        return f'{self.name}'


class Order(models.Model):
    order_number=models.CharField(verbose_name="订单号",max_length=14,default="114514")
    good=models.ForeignKey(Goods,default=None,null=True,on_delete=models.SET_DEFAULT,related_name="good",verbose_name="商品")
    seller=models.ForeignKey(UserInfo,default=None,null=True,on_delete=models.SET_DEFAULT,related_name="seller",verbose_name="卖家")
    buyer=models.ForeignKey(UserInfo,default=None,null=True,on_delete=models.SET_DEFAULT,related_name="buyer",verbose_name="买家")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="购买时间")

    status_choices = (
        (0, "订单失败"),
        (1, "订单支付中"),
        (2, "订单完成")
    )
    status = models.SmallIntegerField(choices=status_choices, default=1, verbose_name="状态")

    def __str__(self):
        """
            重写__str__方法，这样只要打印这个类的都会显示name字段
        """
        return f'{self.order_number}'

