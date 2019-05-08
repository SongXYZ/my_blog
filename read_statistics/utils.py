import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum, ReadDetail
from blog.models import Blog


# 阅读计数
def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)  # 获取obj模型
    key = "%s_%s_readed" % (ct.model, obj.pk)  # blog_%s_readed 拼接cookie的键值

    if not request.COOKIES.get(key):  # 通过cookie的键值判断cookie是否存在
        # 博客阅读数量计数 每篇博客的总阅读数
        # if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count() != 0:  # 查找该博客是否存在
        #     readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)  # 存在 过去该模型实例
        # else:
        #     readnum = ReadNum(content_type=ct, object_id=obj.pk)  # 不存在　实例化该模型

        # 存在获取，不存在创建
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1  # 计数加1
        readnum.save()  # 保存

        # 博客每天每篇博客数量计数
        date = timezone.now().date()
        if ReadDetail.objects.filter(content_type=ct, object_id=obj.pk, date=date).count() != 0:
            readDetail = ReadDetail.objects.get(content_type=ct, object_id=obj.pk, date=date)
        else:
            readDetail = ReadDetail(content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()
    return key


# 获取7天阅读量
def get_seven_days_read_data(content_type):
    today = timezone.now().date()  # 获取年月日
    dates = []
    read_nums = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)  # 今天减几天
        dates.append(date.strftime('%m/%d'))  # 将日期对象按格式转换成字符串

        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)  # 查找该天的数据
        result = read_details.aggregate(read_num_sum=Sum('read_num'))  # 进行求和
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums


# 获取今天阅读量比较多的几篇博客阅读量
def get_today_hot_data(content_type):
    today = timezone.now().date()  # 获取今天时间 年月日
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')  # 查询
    return read_details[:7]  # 通过切片取前7条


# 获取昨天阅读量比较多的博客
def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_detail = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return read_detail[:7]


# # 获取前7天读量比较多的博客
# def get_week_hot_data(content_type):
#     today = timezone.now().date()
#     week_date = today - datetime.timedelta(days=7)
#     read_detail = ReadDetail.objects\
#                             .filter(content_type=content_type, date__lt=today, date__gte=week_date)\
#                             .values('content_type', 'object_id')\
#                             .annotate(read_num_sum=Sum('read_num'))
#     # 通过object_id将数据按id分组
#     return read_detail[:7]


# 获取前7天读量比较多的博客
def get_week_hot_data(content_type):
    today = timezone.now().date()
    week_date = today - datetime.timedelta(days=7)
    read_detail = Blog.objects\
                      .filter(read_details__date__lt=today, read_details__date__gte=week_date)\
                      .values('id', 'title')\
                      .annotate(read_num_sum=Sum('read_details__read_num'))\
                      .order_by("-read_num_sum")
    # 将数据按id分组
    return read_detail[:7]

