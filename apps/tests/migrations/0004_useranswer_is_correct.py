# Generated by Django 5.0.6 on 2024-06-09 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0003_answeroption_image_alter_question_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
    ]
