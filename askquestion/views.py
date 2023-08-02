from django.shortcuts import render
#from django.contrib.auth.mixins import LoginRequiredMixin カスタムクラスを使用するため不要
from django.views.generic import DetailView,TemplateView

from utils.mixins import CustomLoginRequiredMixin #追加

from questioncard.models import QuestionCard
from deck.models import Deck

# このviewのルーティングは「/myapp/Index」
class IndexView(CustomLoginRequiredMixin, DetailView):

    #model = QuestionCard

    template_name = "askquestion/ask_question.html"

    def get(self, request, *args, **kwargs):
        deck = QuestionCard.objects.get(pk=1)
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        deck = Deck.objects.get(pk=self.kwargs.get('deck_pk'))
        foo = QuestionCard.objects.filter(in_deck=deck)[0]
        return foo
    
    def get_context_data(self, **kwargs):
        """
        表示データの設定
        """
        # 表示データの追加はここで 例：
        # kwargs['sample'] = 'sample'
        return super().get_context_data(**kwargs)