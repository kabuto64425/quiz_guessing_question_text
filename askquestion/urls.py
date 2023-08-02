from django.urls import path

from .views import IndexView

# アプリケーションのルーティング設定

urlpatterns = [
    path('<int:pk>/<int:number>', IndexView.as_view(), name='set_question')
]
