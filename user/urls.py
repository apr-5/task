from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.UserCreateView.as_view()),
    path("signin/", views.UserSigninView.as_view()),
    path("signout/", views.UserSignoutView.as_view()),
]