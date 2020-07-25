from django.urls import path
from .views import home, blog, CreateBlog, EditBlog, DeleteBlog

urlpatterns = [
    path('all/', blog),
    path('create/', CreateBlog.as_view()),
    path('<int:blog_id>/edit/', EditBlog.as_view()),
    path('<int:blog_id>/delete/', DeleteBlog.as_view()),
]
