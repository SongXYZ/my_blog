from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
# from blog.models import Blog
from .models import Comment


def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))

    user = request.user  # 获取用户
    if not user.is_authenticated:
        return render(request, 'error.html', {'message': "未登录", 'redirect_to': referer})

    text = request.POST.get('text', '')  # 获取评论内容
    if text == "":
        return render(request, 'error.html', {'message': "评论内容不能为空", 'redirect_to': referer})

    try:
        content_type = request.POST.get('content_type', '')  # 获取评论对象类型
        object_id = int(request.POST.get('object_id', ''))  # 获取评论对象id
        model_class = ContentType.objects.get(model=content_type).model_class()  # 获得具体的模型　Blog
        model_obj = model_class.objects.get(pk=object_id)  # 根据id获取对应的对象
    except Exception as e:
        return render(request, 'error.html', {'message': "评论对象不存在", 'redirect_to': referer})


    comment = Comment()
    comment.user = user
    comment.text = text
    # Blog.objects.get(pk=object_id)
    comment.content_object = model_obj  # 一起给，也可分开给content_type和object_id
    comment.save()

    return redirect(referer)







