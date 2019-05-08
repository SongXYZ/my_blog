from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail


# Create your models here.
# 博客类别
class BlogType(models.Model):
    type_name = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type_name


# 博客模型
class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    # content = models.TextField()
    # content = RichTextField(default='xxxxxxxxxxxxxxxxxx')
    content = RichTextUploadingField()
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)  # 关联BlogType类型 在一个应用里 在数据库里进行了外键关联
    read_details = GenericRelation(ReadDetail)  # 关联ReadDetail模型 不在一个应用里 没在数据里进行关联
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Blog %s>" % self.title

    # 按时间倒序排序
    class Meta:
        ordering = ['-create_time']

    # 封装此方法　通过类的继承 以通用
    # # BuD
    # def get_read_num(self):
    #     try:
    #         return self.readnum.read_num  # 通过ReadNum的实例获取属性read_num
    #     except exceptions.ObjectDoesNotExist:  # 这里只需要捕获object不存在的异常即可
    #         return 0

    # # BuD
    # def get_read_num(self):
    #     try:
    #         ct = ContentType.objects.get_for_model(self)  # 获取Blog模型
    #         readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
    #         return readnum.read_num  # 通过ReadNum的实例获取属性read_num
    #     except exceptions.ObjectDoesNotExist:  # 这里只需要捕获object不存在的异常即可
    #         return 0


# # 博客阅读数量
# class ReadNum(models.Model):
#     read_num = models.IntegerField(default=0)
#     blog = models.OneToOneField(Blog, on_delete=models.DO_NOTHING)  # 一对一



