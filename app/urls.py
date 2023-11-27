from django.urls import path

from .views import IndexView

# アプリケーションのルーティング設定

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
