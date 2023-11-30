from django.shortcuts import render
#from django.contrib.auth.mixins import LoginRequiredMixin カスタムクラスを使用するため不要
from django.views.generic import TemplateView
from django.urls import reverse
from django.core.exceptions import PermissionDenied

from questioncard.models import QuestionCard
from deck.models import Deck


class TopView(TemplateView):

    template_name = "askquestion/top.html"

    # アクセス権がないユーザーのアクセスを防ぐため
    def get(self, request, *args, **kwargs):
        deck = Deck.objects.get(pk=self.kwargs.get('deck_pk'))
        if deck.public_flag or self.request.user == deck.owner:
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

        kwargs["owner"] = deck.owner
        kwargs["dek_name"] = deck.deck_name

        kwargs["question_number"] = None

        kwargs["next_url"] = reverse('ask_question', kwargs={'deck_pk': self.kwargs.get('deck_pk'), 'number': 1})
        kwargs["prev_url"] = None

        urls = [reverse('ask_question', kwargs={'deck_pk': self.kwargs.get('deck_pk'), 'number': i + 1}) for i in range(len(question_cards))]
        kwargs["urls"] = urls

        return super().get_context_data(**kwargs)

class AskQuestionView(TemplateView):

    template_name = "askquestion/ask_question.html"

    # アクセス権がないユーザーのアクセスを防ぐため
    def get(self, request, *args, **kwargs):
        deck = Deck.objects.get(pk=self.kwargs.get('deck_pk'))
        if deck.public_flag or self.request.user == deck.owner:
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
        
        kwargs["owner"] = deck.owner
        kwargs["questioncard"] = question_cards[self.kwargs.get('number') - 1]

        kwargs["question_number"] = self.kwargs.get('number')

        kwargs["next_url"] = reverse('ask_question', kwargs={'deck_pk': self.kwargs.get('deck_pk'), 'number': self.kwargs.get('number') + 1}) if self.kwargs.get('number') < len(question_cards) else reverse('ask_question_bottom', kwargs={'deck_pk': self.kwargs.get('deck_pk')})
        kwargs["prev_url"] = reverse('ask_question', kwargs={'deck_pk': self.kwargs.get('deck_pk'), 'number': self.kwargs.get('number') - 1}) if self.kwargs.get('number') > 1 else reverse('ask_question_top', kwargs={'deck_pk': self.kwargs.get('deck_pk')})

        urls = [reverse('ask_question', kwargs={'deck_pk': self.kwargs.get('deck_pk'), 'number': i + 1}) for i in range(len(question_cards))]
        kwargs["urls"] = urls

        return super().get_context_data(**kwargs)
    
class BottomView(TemplateView):

    template_name = "askquestion/bottom.html"

    # アクセス権がないユーザーのアクセスを防ぐため
    def get(self, request, *args, **kwargs):
        deck = Deck.objects.get(pk=self.kwargs.get('deck_pk'))
        if deck.public_flag or self.request.user == deck.owner:
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

        kwargs["owner"] = deck.owner
        kwargs["dek_name"] = deck.deck_name

        kwargs["question_number"] = None

        kwargs["next_url"] = None
        kwargs["prev_url"] = reverse('ask_question', kwargs={'deck_pk': self.kwargs.get('deck_pk'), 'number': len(question_cards)})

        urls = [reverse('ask_question', kwargs={'deck_pk': self.kwargs.get('deck_pk'), 'number': i + 1}) for i in range(len(question_cards))]
        kwargs["urls"] = urls

        return super().get_context_data(**kwargs)