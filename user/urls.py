from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user import views


urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path(
        "changepassword/",
        views.UserChangePasswordView.as_view(),
        name="changepassword",
    ),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path(
        "subscription/<int:pk>",
        views.UserChangeSubscriptionView.as_view(),
        name="subscription change",
    ),
]
