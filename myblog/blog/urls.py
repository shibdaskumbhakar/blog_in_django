from django.urls import path, re_path

from . import views
from .views import blogtDetailSlugViews, BlogUpdateView, BlogDeleteView
from django.contrib.auth.views import LogoutView
app_name = "blog"
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', LogoutView.as_view(), name="logout"),
    path('register', views.register, name='register'),
    path('myaccount', views.myaccount, name='myaccount'),
    path('blog/like', views.like, name='like'),
    path('blog/dislike', views.Dislike, name='dislike'),
    path('blog/comment', views.comment, name='comment'),
    path('myaccount/addblog', views.addblog, name='addblog'),
    re_path(r'^(?P<slug>[\w-]+)/$', blogtDetailSlugViews.as_view()),
    re_path(r'^(?P<slug>[\w-]+)/update$',
            BlogUpdateView.as_view(), name='updaet'),
    re_path(r'^(?P<slug>[\w-]+)/delete$',
            BlogDeleteView.as_view(), name='delete'),

]
