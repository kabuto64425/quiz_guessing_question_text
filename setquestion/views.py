from django.shortcuts import render
#from django.contrib.auth.mixins import LoginRequiredMixin カスタムクラスを使用するため不要
from django.views.generic import TemplateView

from utils.mixins import CustomLoginRequiredMixin #追加

# このviewのルーティングは「/myapp/Index」
class IndexView(CustomLoginRequiredMixin, TemplateView):
    template_name = "setquestion/index.html"
