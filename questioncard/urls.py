from django.urls import path

from .views import QuestionCardListView, QuestionCardCreateView, QuestionCardUpdateView

# アプリケーションのルーティング設定

urlpatterns = [
    path('list/deck_<int:deck_pk>/', QuestionCardListView.as_view(), name='question_card_list'),
    path('create/deck_<int:deck_pk>/', QuestionCardCreateView.as_view(), name='question_card_create'),
    path('update/<int:pk>/', QuestionCardUpdateView.as_view(), name='question_card_update'),
]
