from shinku_1.models import MainType
from shinku_1.utils.Forms import MainTypeModelForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from shinku_1.utils.pageination import pageination
from shinku_1 import models
from django.db import models as mod

def maintype_list(request):
    """商品主要类型列表"""
    # 搜索商品 字符串包含搜索{[the fields_name u wanna searching]__contains：value}
    data_dict = {}
    value = request.GET.get('str')
    if value is not None:
        data_dict = {"name__contains": value}
    queryset = models.MainType.objects.filter(**data_dict).all().order_by('id')
    # 获取所有商品信息
    _fields = models.MainType._meta.get_fields()
    _fields = [field for field in MainType._meta.get_fields() if not isinstance(field, mod.ManyToOneRel)]
    # 显示
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
        "form": MainTypeModelForm(),
        "btn_show_size": btn_show_size,
        "user_input": user_input,
    }
    return render(request, "HTML/admin/maintype_list.html", context)


# @csrf_exempt
def maintype_list_add(request):
    """添加商品"""

    form = MainTypeModelForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


def maintype_list_delete(request,uid):

    print(uid)
    """删除数据"""
    if not models.MainType.objects.filter(id=uid).exists():

        return JsonResponse({'status': False, 'error': "数据不存在"})
    elif models.Goods.objects.filter(id=uid).exists():

        number = models.Goods.objects.filter(main_type=uid).count()
        return JsonResponse({'status': False, 'error': "该分类还存在" + str(number) + "件商品,不能删除"})
    else:
        models.MainType.objects.filter(id=uid).delete()
        return JsonResponse({'status': True})


def maintype_list_edit(request, uid):
    """修改数据"""
    # 找到数据转换为字典
    row_object = models.MainType.objects.filter(id=uid).values("name").first()
    if request.method == 'GET':
        if row_object is None:
            return JsonResponse({'status': False, 'error': "数据不存在。"})

        result = {
            "status": True,
            "data": row_object
        }
        return JsonResponse(result)

    # IF POST/
    # 转换为对象
    row_object = models.MainType.objects.filter(id=uid).first()

    form = MainTypeModelForm(data=request.POST, instance=row_object)
    # 校验
    if row_object is None:
        return JsonResponse({'status': False, 'tips': "数据不存在。"})
    if form.is_valid():
        # 通过校验
        form.save()
        return JsonResponse({'status': True})
    # 未通过返回错误信息
    return JsonResponse({'status': False, 'error': form.errors})
