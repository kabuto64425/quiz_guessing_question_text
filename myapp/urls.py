from django.urls import path

from .views import IndexView

# アプリケーションのルーティング設定

urlpatterns = [
    path('top', IndexView.as_view(), name='top')
]
