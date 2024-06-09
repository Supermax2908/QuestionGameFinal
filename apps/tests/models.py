from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
# Create your models here.

class Test(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors_tests', null=False)
    topic = models.CharField(max_length=20)
    description = models.TextField(max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.topic} - {self.author}'
    
    class Meta:
        ordering=['-created_at']
    
class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    content = models.CharField(max_length=250, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_questions')
    image = ProcessedImageField(
        upload_to='posts',
        processors=[ResizeToFill(800, 400)],
        format='WEBP',
        options={'quality': 60},
        null=True,
        blank=True
    )
    
    slug = models.SlugField(unique=True, max_length=255, default=None)

    def __str__(self):
        return f"{self.content} - {self.test.topic} - {self.test.author}"

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return 'https://via.placeholder.com/800x400.jpg'
        
        
class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255, blank=True, null=True)
    option_image =  ProcessedImageField(
        upload_to='posts',
        processors=[ResizeToFill(800, 400)],
        format='WEBP',
        options={'quality': 60},
        null=True,
        blank=True
    )
    image = ProcessedImageField(
        upload_to='posts',
        processors=[ResizeToFill(800, 400)],
        format='WEBP',
        options={'quality': 60},
        null=True,
        blank=True
    )
    
    is_correct = models.BooleanField(default=False)
    
    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return 'https://via.placeholder.com/800x400.jpg'
        
    
    def __str__(self):
        return f'{self.option_text}'
    

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_option = models.ForeignKey(AnswerOption, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

class UserScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    

