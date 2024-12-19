'''自定义分页组件'''
"""
////in view
    queryset = models.goods.objects.filter(**data_dict)

   page_object = pageination(request=request, queryset=queryset)  #初始化类

    page_queryset = page_object.page_queryset                     #获取显示数据据
    page_string = page_object.html()                              #页码组件
    context = {
        "goods_fields": _fields,    #所有表头
        "goods": page_queryset,     #每一页数据
        "page_string": page_string, #分页
    }
    return render(request, "goods_list.html", context)
////in html
        
        <nav aria-label="Page navigation example">
        <ul class="pagination justify-content-center">

            {{ page_string }}
            
        </ul>
    </nav>
    
"""
from django.utils.safestring import mark_safe


class pageination(object):

    def __init__(self, request, queryset, page_data_size=10, page_param="page", show_size="page_data_size"):
        """
        request:请求对象
        queryset:当前页码的datas
        page_param传递每页多少数据的参数：page_data_size:每页多少个数据
        page_param传递页码的参数：page:页码
        page_show_size分页的页码量/2
        """
        # 获取每页多少个数据
        self.page_param = page_param
        self.show_size = show_size
        import copy
        query_dict = copy.deepcopy(request.GET)
        self.query_dict = query_dict

        query_dict_for_btn = copy.deepcopy(request.GET)
        self.query_dict_for_btn=query_dict_for_btn

        page_data_size = request.GET.get(show_size, "10")

        if page_data_size.isdecimal():
            page_data_size = int(page_data_size)
        else:
            page_data_size = 10
        # 获取当前页
        self.page_data_size = page_data_size

        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        # 计算显示每页起始和结束的列
        self.start = (page - 1) * page_data_size
        self.end = page * page_data_size

        self.page_queryset = queryset[self.start:self.end]

        # 数据总数
        total_count = queryset.count()
        # 总页数
        total_page_count, div = divmod(total_count, page_data_size)
        if div != 0:
            total_page_count += 1
        # 计算出前n后n也
        self.total_page_count = total_page_count





    def html(self, page_show_size=5):

        if self.total_page_count <= 2 * page_show_size:
            # 数据库数据少
            start_page = 1
            end_page = self.total_page_count
        elif self.page <= page_show_size:
            # 数据库数据多
            # -最初的几页
            start_page = 1
            end_page = 2 * page_show_size + 1
        elif (self.page + page_show_size) >= self.total_page_count:
            # -最后的几页
            end_page = self.total_page_count
            start_page = self.total_page_count - 2 * page_show_size
        else:
            # -中间的页数
            start_page = self.page - page_show_size
            end_page = self.page + page_show_size
        pass

        # 分页
        page_str_list = []



        # 首页
        self.query_dict.setlist(self.page_param, [1])
        page_str_list.append(
            '<li class="page-item"><a class="page-link" href="?{}">start</a></li>'.format(self.query_dict.urlencode()))
        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            previous = '<li class="page-item"><a class="page-link" href="?{}">Previous</a></li>'.format(
                self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.page])
            previous = '<li class="page-item"><a class="page-link" href="?{}">Previous</a></li>'.format(
                self.query_dict.urlencode())
        page_str_list.append(previous)
        # 中间页
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="page-item active" aria-current="page"><a class="page-link active" href="?{}">{}</a></li>'.format(
                    self.query_dict.urlencode(), i)
            else:
                ele = '<li class="page-item"><a class="page-link" href="?{}">{}</a></li>'.format(
                    self.query_dict.urlencode(), i)
            page_str_list.append(ele)
        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            previous = '<li class="page-item"><a class="page-link" href="?{}">Next</a></li>'.format(
                self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.page])
            previous = '<li class="page-item"><a class="page-link" href="?{}">Next</a></li>'.format(
                self.query_dict.urlencode())
        page_str_list.append(previous)
        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append(
            '<li class="page-item"><a class="page-link" href="?{}">end</a></li>'.format(self.query_dict.urlencode()))
        serching_page_str = '''            
                    <form method="get">
                        <div class="input-group  container text-center float-right" style="width: 140px;">
                            <input type="text" class="form-control" placeholder="请输入页码" aria-describedby="basic-addon2"
                                   name="page">
                        </div>
                    </form>'''
        page_str_list.append(serching_page_str)
        page_string = mark_safe("".join(page_str_list))


        return page_string

    def BtnSize(self):



        btn_str_list = []

        self.query_dict_for_btn.setlist(self.show_size, [20])
        str_btn_2 = ''' <a href="?{}" class="float-right">
        <button type="button" class="btn btn-outline-danger btn-sm" style="margin-left: 10px">大量显示</button>
        </a>'''.format(self.query_dict_for_btn.urlencode())
        btn_str_list.append(str_btn_2)

        self.query_dict_for_btn.setlist(self.show_size, [10])
        str_btn_1 = ''' <a href="?{}" class="float-right">
        <button type="button" class="btn btn-outline-secondary btn-sm" style="margin-left: 10px">少量显示</button>
        </a>'''.format(self.query_dict_for_btn.urlencode())
        btn_str_list.append(str_btn_1)



        btn_string=mark_safe("".join(btn_str_list))

        return btn_string
