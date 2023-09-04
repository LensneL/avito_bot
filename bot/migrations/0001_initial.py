# Generated by Django 4.2.5 on 2023-09-04 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.PositiveIntegerField(db_index=True, unique=True)),
                ('username', models.CharField(max_length=256)),
                ('first_name', models.CharField(max_length=256)),
                ('last_name', models.CharField(blank=True, max_length=256)),
                ('chat_id', models.PositiveIntegerField(db_index=True, unique=True)),
                ('subscribed', models.BooleanField(default=True)),
            ],
        ),
    ]
