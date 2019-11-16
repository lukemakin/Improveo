from django.urls import path, re_path
from .views import (
    PostCreateView, like_post, GeneralPostUpdateView, GeneralDetailPost, ProblemDetailPost, GeneralPostDelete, PostExampleView)
app_name = "posts"

urlpatterns = [
    path('', PostCreateView.as_view(), name="post-list"),
    path('example/', PostExampleView.as_view(), name="post-example"),
    path('like/', like_post, name="like-post"),
    path('<pk>/update/', GeneralPostUpdateView.as_view(), name="post-update"),
    path('<pk>/detail/', GeneralDetailPost.as_view(), name="gp-detail"),
    path('<pk>/delete/', GeneralPostDelete.as_view(), name="gp-delete"),
    path('<pk1>/<pk>/detail/',
         ProblemDetailPost.as_view(), name="pp-detail"),

]
