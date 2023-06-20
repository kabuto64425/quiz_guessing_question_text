from django.urls import path

from .views import DeckListView, DeckCreateView

# アプリケーションのルーティング設定

urlpatterns = [
    path('list', DeckListView.as_view(), name='deck_list'),
    path('create/', DeckCreateView.as_view(), name='deck_create'),
]
