from django.urls import path

from .views import UserChangeView, LoginView

# アプリケーションのルーティング設定
app_name = 'users'
urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('update', UserChangeView.as_view(), name='update'),
]
