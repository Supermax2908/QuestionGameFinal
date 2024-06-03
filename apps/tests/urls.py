from django.urls import path
from . import views

app_name = 'tests'

urlpatterns = [
    path('test/', views.test, name='test'),
    path('create/test/', views.create_test, name='create_test'),
    path('delete/test/<int:test_id>/', views.delete_test, name='delete_test'),
    
    path('registration/<int:test_id>/', views.registration_test, name='registration_test'),
    
    path('question/<slug:slug>/', views.take_question, name='question'),
    path('create/question/<int:test_id>/', views.create_question, name='create_question'),
    path('delete/question/<slug:slug>/', views.delete_question, name='delete_question')
]