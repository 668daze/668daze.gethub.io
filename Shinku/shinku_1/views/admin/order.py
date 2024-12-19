from win32comext.mapi.mapitags import PR_PROFILE_USER

from shinku_1.utils.Forms import OrderModelForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from shinku_1.utils.pageination import pageination
from shinku_1.models import Order
from django.db import models


def order_list(request):
    """商品主要类型列表"""
    # 搜索商品 字符串包含搜索{[the fields_name u wanna searching]__contains：value}
    data_dict = {}
    value = request.GET.get('str')
    if value is not None:
        data_dict = {"name__contains": value}
    queryset = Order.objects.filter(**data_dict).all().order_by('id')
    # 设定字段
    _fields = ['ID','订单号','卖家','买家','下单时间','订单状态']

    page_object = pageination(request=request, queryset=queryset)

    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    btn_show_size = page_object.BtnSize()

    if value:
        user_input = value
    else:
        user_input = ""

    context = {
        "fields": _fields,  # 所有表头
        "data": page_queryset,  # 每一页数据
        "page_string": page_string,  # 分页
        "form": OrderModelForm(),
        "btn_show_size": btn_show_size,
        "user_input": user_input,
    }
    return render(request, "HTML/admin/order_list.html", context)


# @csrf_exempt
def order_list_add(request):
    """添加商品"""

    form = OrderModelForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


def order_list_delete(request,uid):
    """删除数据"""

    if not Order.objects.filter(id=uid).exists():

        return JsonResponse({'status': False, 'error': "数据不存在"})
    else:
        Order.objects.filter(id=uid).delete()
        return JsonResponse({'status': True})


def order_list_edit(request, uid):
    """修改数据"""
    # 找到数据转换为字典
    row_object = Order.objects.filter(id=uid).first()
    if request.method == 'GET':
        if row_object is None:
            return JsonResponse({'status': False, 'error': "数据不存在。"})

        result = {
            "status": True,
            "data":{
                "order_number": row_object.order_number,
                "seller":row_object.seller.id,
                "buyer":row_object.buyer.id,
            }
        }
        return JsonResponse(result)

    # IF POST/
    # 转换为对象
    row_object = Order.objects.filter(id=uid).first()

    form = OrderModelForm(data=request.POST, instance=row_object)
    # 校验
    if row_object is None:
        return JsonResponse({'status': False, 'tips': "数据不存在。"})
    if form.is_valid():
        # 通过校验
        form.save()
        return JsonResponse({'status': True})
    # 未通过返回错误信息
    return JsonResponse({'status': False, 'error': form.errors})
