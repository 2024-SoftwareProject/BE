# Generated by Django 5.0.2 on 2024-03-17 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='board_type',
            field=models.CharField(blank=True, choices=[('free_board', '자유 게시판'), ('question_board', '질문 게시판'), ('review_board', '판매 게시판')], max_length=20, null=True),
        ),
    ]
