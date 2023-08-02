from django.urls import path

from .views import IndexView

# アプリケーションのルーティング設定

urlpatterns = [
    path('<int:deck_pk>/<int:number>', IndexView.as_view(), name='set_question')
]
