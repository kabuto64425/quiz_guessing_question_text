from django.shortcuts import render
#from django.contrib.auth.mixins import LoginRequiredMixin カスタムクラスを使用するため不要
from django.views.generic import TemplateView

from .mixins import CustomLoginRequiredMixin #追加

# このviewのルーティングは「/myapp/Index」
class IndexView(CustomLoginRequiredMixin, TemplateView):
    template_name = "myapp/index.html"

class VueTestView(CustomLoginRequiredMixin, TemplateView):
    template_name = "myapp/vuetest.html"
