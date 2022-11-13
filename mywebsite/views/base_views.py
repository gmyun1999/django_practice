from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from mywebsite.models import Question


def index(request):
    page = request.GET.get("page", 1)
    kw = request.GET.get("kw", '')
    question_list = Question.objects.order_by('create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(answer__content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()
    paginator = Paginator(question_list, 15)
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'mywebsite/question_list.html', context)


def detail(request, question_id):
    if request.method == "POST":
        pass
    else:
        question = Question.objects.get(id=question_id)
        return render(request, 'mywebsite/question_detail.html', {'question': question})
