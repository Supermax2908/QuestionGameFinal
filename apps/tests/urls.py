from django.urls import path
from . import views

app_name = 'tests'

urlpatterns = [
    path('test/', views.test, name='test'),
    path('create/test/', views.create_test, name='create_test'),
    path('delete/test/<int:test_id>/', views.delete_test, name='delete_test'),
    
    path('registration/<int:test_id>/', views.registration_test, name='registration_test'),
]