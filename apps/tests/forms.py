from django import forms
from .models import Test, Question, AnswerOption

class TestForm(forms.ModelForm):
    class Meta:
        model=Test
        fields = ('topic', 'description')
        
class QuestionForm(forms.ModelForm):
    class Meta:
        model=Question
        fields = ('content', 'image')
        

class AnswerForm(forms.ModelForm):
    class Meta:
        model = AnswerOption
        fields = ['option_text', 'option_image', 'is_correct']
        