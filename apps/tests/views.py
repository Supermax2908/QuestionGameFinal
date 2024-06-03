from django.shortcuts import render, get_object_or_404, redirect
import uuid

from .models import Test
from .forms import TestForm

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
