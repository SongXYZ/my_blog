from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.fields import exceptions
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

# Create your models here.


# 博客阅读数量  ContentType
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    # BuD
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


# 封装的方法
class ReadNumExpandMethod():
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)  # 获取Blog模型
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)  # 获取ReanNum对象的实例
            return readnum.read_num  # 通过ReadNum的实例获取属性read_num
        except exceptions.ObjectDoesNotExist:  # 这里只需要捕获object不存在的异常即可
            return 0


# 每天每篇博客的阅读数量统计
class ReadDetail(models.Model):
    date = models.DateField(default=timezone.now)
    read_num = models.IntegerField(default=0)
    # BuD
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

