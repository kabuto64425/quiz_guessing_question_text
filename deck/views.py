from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView ,DeleteView
from django_filters.views import FilterView
from django.core.exceptions import PermissionDenied

from utils.mixins import CustomLoginRequiredMixin
from users.models import User

from .filters import DeckFilterSet
from .forms import DeckForm
from .models import Deck

class DeckListView(CustomLoginRequiredMixin, FilterView):
    """
    ビュー：一覧表示画面

    以下のパッケージを使用
    ・django-filter 一覧画面(ListView)に検索機能を追加
    https://django-filter.readthedocs.io/en/master/
    """
    model = Deck

    # django-filter 設定
    filterset_class = DeckFilterSet
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
        user = self.request.user  # ログインユーザーモデルの取得
        return Deck.objects.select_related("owner").prefetch_related("in_deck").all().filter(owner = user).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        表示データの設定
        """
        # 表示データを追加したい場合は、ここでキーを追加しテンプレート上で表示する
        # 例：kwargs['sample'] = 'sample'
        return super().get_context_data(object_list=object_list, **kwargs)

class DeckCreateView(CustomLoginRequiredMixin, CreateView):
    """
    ビュー：登録画面
    """
    model = Deck
    form_class = DeckForm
    success_url = reverse_lazy('deck_list')

    def form_valid(self, form):
        """
        登録処理
        """
        deck = form.save(commit=False)
        deck.owner = self.request.user
        deck.created_at = timezone.now()
        deck.updated_at = timezone.now()
        deck.save()

        return HttpResponseRedirect(self.success_url)

class DeckUpdateView(CustomLoginRequiredMixin, UpdateView):
    """
    ビュー：更新画面
    """
    model = Deck
    form_class = DeckForm
    success_url = reverse_lazy('deck_list')

    # 自身のデッキに対してほかユーザーがアクセスするのを防ぐため
    def get(self, request, *args, **kwargs):
        deck = super().get_object()
        if self.request.user == deck.owner:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        """
        更新処理
        """
        deck = form.save(commit=False)
        deck.updated_at = timezone.now()
        deck.save()

        return HttpResponseRedirect(self.success_url)

class DeckDeleteView(CustomLoginRequiredMixin, DeleteView):
    """
    ビュー：削除画面
    """
    model = Deck
    success_url = reverse_lazy('deck_list')

    # 自身のデッキに対してほかユーザーがアクセスするのを防ぐため
    def get(self, request, *args, **kwargs):
        deck = super().get_object()
        if self.request.user == deck.owner:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied