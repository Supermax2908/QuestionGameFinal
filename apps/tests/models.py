from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Test(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors_tests', null=False)
    topic = models.CharField(max_length=20)
    description = models.TextField(max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.topic
    
    class Meta:
        ordering=['-created_at']
        

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors_questions', default=None)
    
    image = models.ImageField(upload_to='question_images/', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')
        
    def __str__(self):
        return f'{self.content} - {self.test.topic} - {self.test.author}'
    
    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return 'https://via.placeholder.com/800x400.jpg'


