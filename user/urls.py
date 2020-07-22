from django.urls import path
from .views import LoginView, ProfileView, SignUpView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('signup/', SignUpView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('logout/', ProfileView.logout_view)
]
