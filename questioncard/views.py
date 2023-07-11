from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView
from django_filters.views import FilterView

from utils.mixins import CustomLoginRequiredMixin
from users.models import User
from deck.models import Deck

from .filters import QuestionCardFilterSet
from .forms import QuestionCardForm
from .models import QuestionCard

class QuestionCardListView(CustomLoginRequiredMixin, FilterView):
    """
    ビュー：一覧表示画面

    以下のパッケージを使用
    ・django-filter 一覧画面(ListView)に検索機能を追加
    https://django-filter.readthedocs.io/en/master/
    """
    model = QuestionCard

    # django-filter 設定
    filterset_class = QuestionCardFilterSet
    # django-filter ver2.0対応 クエリ未設定時に全件表示する設定
    strict = False

    # 1ページの表示
    paginate_by = 10

    def get(self, request, **kwargs):
        """
        リクエスト受付
        セッション変数の管理:一覧画面と詳細画面間の移動時に検索条件が維持されるようにする。
        """

        # 一覧画面内の遷移(GETクエリがある)ならクエリを保存する
        if request.GET:
            request.session['query'] = request.GET
        # 詳細画面・登録画面からの遷移(GETクエリはない)ならクエリを復元する
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)

    def get_queryset(self):
        """
        ソート順・デフォルトの絞り込みを指定
        """
        # デフォルトの並び順として、登録時間（降順）をセットする。
        deck = Deck.objects.get(pk=self.kwargs.get('deck_pk'))
        return QuestionCard.objects.all().filter(in_deck = deck)

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        表示データの設定
        """
        # 表示データを追加したい場合は、ここでキーを追加しテンプレート上で表示する
        # 例：kwargs['sample'] = 'sample'
        return super().get_context_data(object_list=object_list, **kwargs)

class QuestionCardCreateView(CustomLoginRequiredMixin, CreateView):
    """
    ビュー：登録画面
    """
    model = QuestionCard
    form_class = QuestionCardForm

    def get_success_url(self):
        deck_pk = self.kwargs.get('deck_pk')
        return reverse('question_card_list', kwargs={'deck_pk': deck_pk})
    
    def get_context_data(self, *, object_list=None, **kwargs):
        """
        表示データの設定
        """
        # 表示データを追加したい場合は、ここでキーを追加しテンプレート上で表示する
        # 例：kwargs['sample'] = 'sample'
        kwargs['deck_pk'] = self.kwargs.get('deck_pk')
        return super().get_context_data(object_list=object_list, **kwargs)

    def form_valid(self, form):
        """
        登録処理
        """
        question_card = form.save(commit=False)
        deck = Deck.objects.get(pk=self.kwargs.get('deck_pk'))
        question_card.in_deck = deck
        question_card.created_at = timezone.now()
        question_card.updated_at = timezone.now()
        question_card.save()
        return super().form_valid(form)

class QuestionCardUpdateView(CustomLoginRequiredMixin, UpdateView):
    """
    ビュー：更新画面
    """
    model = QuestionCard
    form_class = QuestionCardForm

    def get_success_url(self):
        deck = self.object.in_deck
        return reverse('question_card_list', kwargs={'deck_pk': deck.pk})
    
    def get_context_data(self, *, object_list=None, **kwargs):
        """
        表示データの設定
        """
        # 表示データを追加したい場合は、ここでキーを追加しテンプレート上で表示する
        # 例：kwargs['sample'] = 'sample'
        deck = self.object.in_deck
        kwargs['deck_pk'] = deck.pk
        return super().get_context_data(object_list=object_list, **kwargs)

    def form_valid(self, form):
        """
        更新処理
        """
        question_card = form.save(commit=False)
        question_card.updated_at = timezone.now()
        question_card.save()
        return super().form_valid(form)