from django.shortcuts import render_to_response, get_object_or_404, render
from .models import BlogType, Blog
from django.core.paginator import Paginator
from django.db.models import Count
from read_statistics.utils import read_statistics_once_read  # 封装好的函数
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment

# Create your views here.
# 显示博客列表
def blog_list(request):
    page_num = request.GET.get('page', 1)  # 获取参数(GET)
    blogs_list = Blog.objects.all()
    paginator = Paginator(blogs_list, 10)  # 初始化分页器对象
    page_of_blogs = paginator.get_page(page_num)

    context = {}
    context['page_of_blogs'] = page_of_blogs
    context['blogs'] = page_of_blogs.object_list  # 获取某页所有博客列表
    context['blogs_count'] = Blog.objects.all().count()  # 计算博客数量，可在模板页面通过过滤器实现

    # 获取博客分类的对应的数量
    # 会转换成sql语句执行 效率比下面方式高, 同样是添加属性blog_count
    context['blog_type'] = BlogType.objects.annotate(blog_count=Count('blog'))

    # # 获取博客分类的对应的数量
    # blog_types_list = []
    # for blog_type in BlogType.objects.all():
    #     # blog_type是博客类别的实例化对象
    #     # 给blog_type对象添加一个blog_count的属性
    #     blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
    #     blog_types_list.append(blog_type)
    # context['blog_type'] = blog_types_list

    # context['blog_type'] = BlogType.objects.all()  # 博客类别列表

    # 获取日期归档对应的博客数量
    blog_dates_list = {}
    for blog_date in Blog.objects.dates('create_time', 'month', order="DESC"):
        # blog_date不是对象
        blog_count = Blog.objects.filter(create_time__year=blog_date.year, create_time__month=blog_date.month).count()
        blog_dates_list[blog_date] = blog_count
    context['blogs_date'] = blog_dates_list

    # 返回博客的 有的日期 第二个参数是作用域 作用到月
    # context['blogs_date'] = Blog.objects.dates('create_time', 'month', order="DESC")
    return render_to_response('blog/blog_list.html', context)  # 会在全局templates目录下寻找blog_list.html模板页面


# 显示博客内容
def blog_detail(request, blog_pk):
    # blog_content = Blog.objects.get(pk=blog_id)
    blog_content = get_object_or_404(Blog, pk=blog_pk)  # 通过博客id，读取
    # # 判断cookie是否存在
    # if not request.COOKIES.get('blog_%s_readed' % blog_pk):
    #     if ReadNum.objects.filter(blog=blog_content).count() != 0:
    #         # 存在记录 查找该博客
    #         readnum = ReadNum.objects.filter(blog=blog_content)
    #     else:
    #         # 不存在对应记录 创建该博客计数
    #         readnum = ReadNum(blog=blog_content)
    #     # 计数加1
    #     readnum.read_num += 1
    #     readnum.save()

    # if not request.COOKIES.get('blog_%s_readed' % blog_pk):
    #     ct = ContentType.objects.get_for_model(Blog)
    #     if ReadNum.objects.filter(content_type=ct, object_id=blog_content.pk).count() != 0:  # 查找该博客是否存在
    #         readnum = ReadNum.objects.get(content_type=ct, object_id=blog_content.pk)  # 存在 获取该模型实例
    #     else:
    #         readnum = ReadNum(content_type=ct, object_id=blog_content.pk)  # 不存在　实例化该模型
    #     readnum.read_num += 1  # 计数
    #     readnum.save()  # 保存
    read_cookie_key = read_statistics_once_read(request, blog_content)  # 通过调用封装好的函数

    blog_content_type = ContentType.objects.get_for_model(blog_content)
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog_content.pk)

    context = {}
    context['blog'] = blog_content
    # filter 筛选条件 id__in=[1, 3] id在1或3里
    # 上一篇博客 比当前博客时间大的最后一条
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog_content.create_time).last()
    # 下一篇博客 [0]方式会导致第一篇indexerror
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog_content.create_time).first()
    context['user'] = request.user  # 获取当前登录用户
    context['comments'] = comments

    repos = render(request, 'blog/blog_detail.html', context)
    # 设置cookie
    repos.set_cookie(read_cookie_key, 'true')  # 参数expires指定时间过期  参数max_age多长时间后过期(秒)
    return repos


# 显示某个类别下的文章
def blogs_with_type(request, blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)  # 通过博客类别id,取出某个博客类别名
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)  # 过滤器筛选出某个博客类别的文章
    context['blog_type'] = blog_type
    return render_to_response('blog/blogs_with_type.html', context)


# 显示某个月的博客
def blogs_with_date(request, year, month):
    context = {}
    blogs_all_list = Blog.objects.filter(create_time__year=year, create_time__month=month)
    context['blogs_list'] = blogs_all_list
    return render_to_response('blog/blogs_with_date.html', context)



