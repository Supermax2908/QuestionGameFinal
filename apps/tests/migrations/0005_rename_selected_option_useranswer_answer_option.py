# Generated by Django 5.0.6 on 2024-06-09 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0004_useranswer_is_correct'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useranswer',
            old_name='selected_option',
            new_name='answer_option',
        ),
    ]
