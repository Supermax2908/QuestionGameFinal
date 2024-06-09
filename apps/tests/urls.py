from django.urls import path
from . import views

app_name = 'tests'

urlpatterns = [
    path('test/', views.test, name='test'),
    path('create/test/', views.create_test, name='create_test'),
    path('delete/test/<int:test_id>/', views.delete_test, name='delete_test'),
    
    path('registration/<int:test_id>/', views.registration_test, name='registration_test'),
    
    path('create/question/<int:test_id>/', views.create_question, name='create_question'),
    
    path('make_answers/<int:question_id>/', views.make_answers, name='make_answers'),
    path('create_answer/<int:question_id>/', views.create_answer, name='create_answer'),
    path('question/<int:question_id>/submit_answer/', views.submit_answer, name='submit_answer'),
    
    path('result/<int:test_id>/', views.test_result, name='test_result')
]