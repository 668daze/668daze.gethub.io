from shinku_1.utils.Forms import GoodsModelForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from shinku_1.utils.pageination import pageination
from shinku_1 import models


def goods_list(request):
    # for i in range(1,300):
    #     models.goods.objects.create(name="test"+str(i),price=2,description="is just a tset qwq")

    # models.goods.objects.all().delete()
    """商品界面"""
    # 搜索商品 字符串包含搜索{[the fields_name u wanna searching]__contains：value}
    data_dict = {}
    value = request.GET.get('str')
    if value is not None:
        data_dict = {"name__contains": value}
    queryset = models.Goods.objects.filter(**data_dict)
    # 获取所有商品信息
    _fields = ['ID','商品名称','卖家ID','价格','创建时间','商品描述','商品分类','商品状态',]

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
        "goods_fields": _fields,  # 所有表头
        "goods": page_queryset,  # 每一页数据
        "page_string": page_string,  # 分页
        "form": GoodsModelForm(),
        "btn_show_size": btn_show_size,
        "user_input": user_input,
    }
    return render(request, "HTML/admin/goods_list.html", context)


def goods_add(request):
    """添加商品"""
    # 通过链接访问页面
    if request.method == 'GET':
        form = GoodsModelForm()
        return render(request, "HTML/admin/goods_add.html", {'form': form})
    # IF POST\提交表单
    form = GoodsModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin_goods')
    # 输入错误
    return render(request, "HTML/admin/goods_add.html", {'form': form})


def goods_delete(request, uid):
    """删除数据"""
    if models.Goods.objects.filter(id=uid).exists():
        models.Goods.objects.filter(id=uid).delete()
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False, 'error': "数据不存在"})


def goods_edit(request, uid):
    """修改数据"""
    # 链接访问页面
    if request.method == 'GET':
        # 找到数据
        row_object = models.Goods.objects.filter(id=uid).first()
        form = GoodsModelForm(instance=row_object)
        return render(request, "HTML/admin/goods_edit.html", {'form': form})
    # IF POST/
    row_object = models.Goods.objects.get(id=uid)
    form = GoodsModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin_goods')
    # 未通过
    return render(request, "HTML/admin/goods_edit.html", {'form': form})
