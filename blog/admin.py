from django.contrib import admin
from .models import BlogType, Blog


# Register your models here.
@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'create_time')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    # readnum是ReadNum模型的
    list_display = ('title', 'blog_type', 'author', 'content', 'get_read_num', 'create_time', 'last_update_time')


# @admin.register(ReadNum)
# class ReadNumAdmin(admin.ModelAdmin):
#     list_display = ('read_num', 'blog')

