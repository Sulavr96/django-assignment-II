from django.urls import path, include
from .views import LoginView, ProfileView, SignUpView, UserView, AccountActivate, UserUpdate, UserDelete
from blog.views import user_blog

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('signup/', SignUpView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('logout/', ProfileView.logout_view),
    path('', UserView.as_view()),
    path('<int:user_id>/blogs/', user_blog),  
    path('activate/', AccountActivate.as_view()),
    path('update/', UserUpdate.as_view()), 
    path('delete/', UserDelete.as_view()),
]
