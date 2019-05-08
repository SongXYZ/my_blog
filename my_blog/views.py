from django.shortcuts import render_to_response, render, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.urls import reverse
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data, get_week_hot_data
from blog.models import Blog
from .forms import LoginForm


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)  # 调用自定义方法
    today_hot_data = get_today_hot_data(blog_content_type)
    yesterday_hot_data = get_yesterday_hot_data(blog_content_type)
    week_hot_data = get_week_hot_data(blog_content_type)

    context = {
        'read_nums': read_nums,
        'dates': dates,
        'today_hot_data': today_hot_data,
        'yesterday_hot_data': yesterday_hot_data,
        'week_hot_data': week_hot_data
    }
    return render_to_response('home.html', context)


def login(request):
    '''
    # username = request.POST.get('username', '')  # 获取参数username，没有给空
    # password = request.POST.get('password', '')
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(request, username=username, password=password)
    referer = request.META.get('HTTP_REFERER', reverse('home'))  # 重定向到当前页面
    if user is not None:
        auth.login(request, user)
        # Redirect to a success page.
        return redirect(referer)
    else:
        # Return an 'invalid login' error message.
        return render(request, 'error.html', {'message': "用户名或密码错误", 'redirect_to': referer})
    '''

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # username = login_form.cleaned_data['username']
            # password = login_form.cleaned_data['password']
            # user = auth.authenticate(request, username=username, password=password)
            # if user is not None:
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
            # else:
            #     # Return an 'invalid login' error message.
            #     login_form.add_error(None, "用户名或密码错误")
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)






