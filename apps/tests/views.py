from django.shortcuts import render, get_object_or_404, redirect
import uuid

from .models import Test, Question, AnswerOption, UserAnswer, UserScore
from .forms import TestForm, QuestionForm, AnswerForm

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


def registration_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    
    if request.method == 'POST':
        if test.author == request.user:
            return redirect('tests:create_question', test_id=test_id)
        else:
            questions = Question.objects.filter(test=test)
            if questions.exists():
                for question in questions:
                    return redirect('tests:make_answers', question_id=question.id)
            else:
                messages.error(request, 'В тесті нема питань.')

    return render(request, 'tests/registration_test.html', {'test': test})
        
        
@login_required
def create_question(request, test_id):
    test = get_object_or_404(Test, pk=test_id, author=request.user)
    
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.test = test
            question.author = request.user
            question.slug = uuid.uuid4().hex
            question.save()
            return redirect('tests:create_answer', question_id=question.id)
    else:
        form = QuestionForm()
    return render(request, 'tests/question.html', {'test': test, 'question_form': form})
    

@login_required
def make_answers(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    options = AnswerOption.objects.filter(question=question)
    return render(request, 'tests/answer.html', {'question': question, 'options': options})


def create_answer(request, question_id):
    question = Question.objects.get(pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
    else:
        form = AnswerForm()
    
    return render(request, 'tests/answer.html', {'create_answer_form': form, 'question': question})

@login_required
def submit_answer(request, question_id):
    if request.method == 'POST':
        option_id = request.POST.get('option_id')
        
        question = get_object_or_404(Question, pk=question_id)
        option = get_object_or_404(AnswerOption, pk=option_id)
        
        user_answer, created = UserAnswer.objects.get_or_create(
            user=request.user,
            question=question,
            defaults={'answer_option': option}
        )
        
        if not created:
            user_answer.answer_option = option
            user_answer.save()
        
        if option.is_correct:
            user_score, score_created = UserScore.objects.get_or_create(
                user=request.user,
                test=question.test
            )
            user_score.score += 1
            user_score.save()
            messages.success(request, 'Ви отримали 1 бал.')
        else:
            messages.error(request, 'Ви відповіли неправильно!')
        
        next_question = Question.objects.filter(test=question.test, id__gt=question.id).order_by('id').first()
        
        if next_question:
            return redirect('tests:make_answers', question_id=next_question.id)
        else:
            messages.success(request, 'Ви відповіли на всі питання тесту!')
            return redirect('tests:test_result', test_id=question.test.id)
    return redirect('introduction:welcome')

@login_required
def test_result(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    questions = Question.objects.filter(test=test)
    results = {}
    total_questions = len(questions)
    
    correct_answers_count = 0
    for question in questions:
        user_answers = request.POST.getlist(str(question.id))
        correct_answers = AnswerOption.objects.filter(question=question, is_correct=True)
        is_correct = set(user_answers) == set(str(answer.id) for answer in correct_answers) # values_list повертає список значень полів для об'єктів, які задовольняють фільтрації запиту
        
        if is_correct:
            correct_answers_count == 0
        else:
            correct_answers_count += 1
            
        results[question] = is_correct
        
        
            
    user_score = int(correct_answers_count / total_questions) * 100

    context = {
        'test': test, 
        'results': results, 
        'total_questions': total_questions, 
        'correct_answers': correct_answers_count, 
        'user_score': user_score
    }
    return render(request, 'tests/test_result.html', context)
