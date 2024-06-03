from django.shortcuts import render, get_object_or_404, redirect
import uuid

from .models import Test, Question
from .forms import TestForm, QuestionForm

from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

@login_required
def test(request):
    all_tests = Test.objects.all()
    context = {
        'all_tests': all_tests,
        'created_form': TestForm
    }
    return render(request, 'tests/test.html', context)

@login_required
def create_test(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.author = request.user
            test.save()
            messages.success(request, 'Автор опублікував новий тест')
            return redirect('tests:test')
        else:
            messages.error(request, 'Не вдалося створити тест')
    else:
        form = TestForm()
    return render(request, 'tests/create_test.html', {'form': form})

@login_required
def delete_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id, author=request.user)
    if request.method == 'POST':
        test.delete()
        messages.success(request, 'Тест успішно видалено.')
    else:
        messages.error(request, 'Помилка видалення тесту.')
    return redirect('tests:test')


@login_required
def registration_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    if request.method == 'POST':
        if test.author == request.user:
            return redirect('tests:create_question', test_id=test.id)
        else:
            questions = Question.objects.filter(test=test)
            for question in questions:
                messages.success(request, 'Починаємо!')
                return redirect('tests:question', slug=question.slug)
    return render(request, 'tests/registration_test.html', {'test': test})

@login_required
def take_question(request, slug):
    question = get_object_or_404(Question, slug=slug)
    return render(request, 'tests/question.html', {'question': question})

@login_required
def create_question(request, test_id):
    test = get_object_or_404(Test, pk=test_id, author=request.user)
    if request.method == "POST":
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.slug = uuid.uuid4().hex
            question.test = test
            question.author = request.user
            question.save()
            return redirect('tests:question', slug=question.slug)
    else:
        form = QuestionForm()
    return render(request, 'tests/question.html', {'test': test, 'question_form': form})

@login_required
def delete_question(request, slug):
    question = get_object_or_404(Question, slug=slug, author=request.user)
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Питання видалено успішно.') 
    else:
        messages.error(request, 'Помилка видалення питання.')
    return redirect('tests:test') 
