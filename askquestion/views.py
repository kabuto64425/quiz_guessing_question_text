from django.shortcuts import render
#from django.contrib.auth.mixins import LoginRequiredMixin カスタムクラスを使用するため不要
from django.views.generic import DetailView,TemplateView
from django.urls import reverse
from django.core.exceptions import PermissionDenied

from utils.mixins import CustomLoginRequiredMixin #追加

from questioncard.models import QuestionCard
from deck.models import Deck

# このviewのルーティングは「/myapp/Index」
class IndexView(CustomLoginRequiredMixin, TemplateView):

    #model = QuestionCard

    template_name = "askquestion/ask_question.html"

    # 自身のデッキに対してほかユーザーがアクセスするのを防ぐため
    def get(self, request, *args, **kwargs):
        deck = Deck.objects.get(pk=self.kwargs.get('deck_pk'))
        if self.request.user == deck.owner:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied
    
    def get_context_data(self, **kwargs):
        """
        表示データの設定
        """
        # 表示データの追加はここで 例：
        # kwargs['sample'] = 'sample'
        deck = Deck.objects.get(pk=self.kwargs.get('deck_pk'))
        question_cards = QuestionCard.objects.filter(in_deck=deck).order_by('order')
        
        kwargs["questioncard"] = question_cards[self.kwargs.get('number') - 1]

        kwargs["question_number"] = self.kwargs.get('number')

        kwargs["next_url"] = reverse('ask_question', kwargs={'deck_pk': self.kwargs.get('deck_pk'), 'number': self.kwargs.get('number') + 1}) if self.kwargs.get('number') < len(question_cards) else None
        kwargs["prev_url"] = reverse('ask_question', kwargs={'deck_pk': self.kwargs.get('deck_pk'), 'number': self.kwargs.get('number') - 1}) if self.kwargs.get('number') > 1 else None

        urls = [reverse('ask_question', kwargs={'deck_pk': self.kwargs.get('deck_pk'), 'number': i + 1}) for i in range(len(question_cards))]
        kwargs["urls"] = urls

        return super().get_context_data(**kwargs)