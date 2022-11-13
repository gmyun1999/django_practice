from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from mywebsite.forms import AnswerForm
from mywebsite.models import Question, Answer


@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    form = AnswerForm(request.POST)
    if form.is_valid():
        answer = form.save(commit=False)
        answer.create_date = timezone.now()
        answer.question = question
        answer.author = request.user
        answer.save()
        return redirect(f"{resolve_url('mywebsite:detail', question_id=question.id)}#answer_{answer.id}")
    context = {'form': form, 'question': question}
    return render(request, 'mywebsite/question_detail.html', context)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages(request, "수정권한이 없습니다.")
        return redirect('mywebsite:detail', question_id=answer.question.id)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.author = request.user
            answer.save()
            return redirect(f"{resolve_url('mywebsite:detail', question_id=answer.question.id)}#answer_{answer.id}")

    else:
        form = AnswerForm(instance=answer)
    context = {'form': form, 'answer': answer}
    return render(request, 'mywebsite/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages(request, "삭제권한이 없습니다")
    else:
        answer.delete()
    return redirect('mywebsite:detail', question_id=answer.question.id)
