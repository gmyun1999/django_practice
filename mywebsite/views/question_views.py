from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from mywebsite.forms import QuestionForm
from mywebsite.models import Question


@login_required(login_url='common:login')
def question_create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.author = request.user
            question.save()
            return redirect('mywebsite:index')
    else:
        form = QuestionForm()
    return render(request, 'mywebsite/question_form.html', {'form': form})


@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "수정권한이 없습니다.")
        return redirect('mywebsite:detail', question_id=question.id)
    if request.method == "POST":  # 수정하기 눌러서 form 받은후에 서버로 다시 넘어왔을때
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('mywebsite:index')
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'mywebsite/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages(request, "삭제권한이 없습니다")
        return redirect("mywebsite:detail", question_id=question.id)
    question.delete()
    return redirect('mywebsite:index')


@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, "본인글에는 좋아요를 누를수없습니다")
    else:
        question.voter.add(request.user)
    return redirect("mywebsite:detail", question_id=question.id)

