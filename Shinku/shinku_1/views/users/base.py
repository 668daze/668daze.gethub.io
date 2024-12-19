from django.shortcuts import render, HttpResponse


def index1(request):
    # return HttpResponse('<h1> hell NO!<\H1>')
    return render(request, 'HTML/users/user_home_page.html')


def index2(request):
    # return HttpResponse('<h1> hell NO!<\H1>')
    return render(request, 'HTML/users/good_page.html')


def index3(request):
    # return HttpResponse('<h1> hell NO!<\H1>')
    return render(request, 'HTML/users/art_page.html')

def index4(request):
    # return HttpResponse('<h1> hell NO!<\H1>')
    return render(request, 'HTML/users/search_page.html')


def user_list(request):
    return HttpResponse("<h1>user_list<\h1>")


def user_add(request):
    return HttpResponse("user_add")
