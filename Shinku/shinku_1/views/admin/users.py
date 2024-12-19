from shinku_1.utils.Forms import AdminUsersModelForm,AdminUsersModelForm2
from django.http import JsonResponse
from django.shortcuts import render, redirect
from shinku_1.utils.pageination import pageination
from shinku_1.models import UserInfo


def users_list(request):
    # for i in range(1,300):
    #     models.goods.objects.create(name="test"+str(i),price=2,description="is just a tset qwq")

    # models.goods.objects.all().delete()
    """商品界面"""
    # 搜索用户 字符串包含搜索{[the fields_name u wanna searching]__contains：value}
    data_dict = {}
    value = request.GET.get('str')
    if value is not None:
        data_dict = {"name__contains": value}
    queryset = UserInfo.objects.filter(**data_dict)
    # 获取所有商品信息
    _fields = UserInfo._meta.get_fields()

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
        "form": AdminUsersModelForm(),
        "btn_show_size": btn_show_size,
        "user_input": user_input,
    }
    return render(request, "HTML/admin/users_list.html", context)


def users_add(request):
    """添加商品"""
    # 通过链接访问页面
    if request.method == 'GET':
        form = AdminUsersModelForm2()
        return render(request, "HTML/admin/users_add.html", {'form': form})
    # IF POST\提交表单
    form = AdminUsersModelForm2(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect('/admin_users')
    # 输入错误
    return render(request, "HTML/admin/users_add.html", {'form': form})


def users_delete(request, uid):
    """删除数据"""
    if UserInfo.objects.filter(id=uid).exists():
        UserInfo.objects.filter(id=uid).delete()
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False, 'error': "数据不存在"})


def users_edit(request, uid):
    """修改数据"""
    # 链接访问页面
    if request.method == 'GET':
        # 找到数据
        row_object = UserInfo.objects.filter(id=uid).first()
        form = AdminUsersModelForm(instance=row_object)
        return render(request, "HTML/admin/users_edit.html", {'form': form})
    # IF POST/
    row_object = UserInfo.objects.get(id=uid)
    form = AdminUsersModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin_users')
    # 未通过
    return render(request, "HTML/admin/users_edit.html", {'form': form})


