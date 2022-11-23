from django.urls import path

from qnasite.views import base_views

app_name = 'qnasite'
urlpatterns = [
    path('', base_views.index, name='index')
]
from django.shortcuts import render


def index(request):
    return render(request, 'qnasite/base.html')
