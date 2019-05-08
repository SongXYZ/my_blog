from django.urls import path
from . import views


urlpatterns = [
    # http://127.0.0.1:8000/blog/
    path('', views.blog_list, name='blog_list'),  # 显示博客列表
    path('<int:blog_pk>', views.blog_detail, name="blog_detail"),  # 显示博客内容
    path('type/<int:blog_type_pk>', views.blogs_with_type, name="blogs_with_type"),  # 显示某个类别下的文章
    path('date/<int:year>/<int:month>', views.blogs_with_date, name="blogs_with_date")
]



