from django.contrib import admin
from .models import Test, Question, AnswerOption, UserAnswer

# Register your models here.


admin.site.register(Test)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('content',),}
    
admin.site.register(AnswerOption)
admin.site.register(UserAnswer)