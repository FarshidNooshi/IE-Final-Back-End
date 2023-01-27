from django.urls import path

from FinalApp.views import RegisterView, LoginView, LogoutView, AuthView, UserView, WebpageView, AlarmView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('auth/', AuthView.as_view()),
    path('webpage/', WebpageView.as_view()),
    path('alarm/', AlarmView.as_view()),
]
