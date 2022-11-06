from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("index/", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:pk>/detail", views.detail, name="detail"),
    path("<int:pk>/update", views.update, name="update"),
    path("<int:pk>/delete", views.delete, name="delete"),
    path("<int:category_pk>/category/", views.category, name="category"),
    path("<int:category_pk>/follow/", views.category_follow, name="category_follow"),
    path("<int:pk>/like/", views.like, name="like"),
    path("comment/<int:pk>", views.comment, name="comment"),
    path("commend_d", views.comment_d, name="comment_d"),
    path("search/", views.search, name="search"),
]
