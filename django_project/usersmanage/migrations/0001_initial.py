# Generated by Django 4.1 on 2022-09-09 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.BigIntegerField(default=1, unique=True, verbose_name='Id пользователя')),
                ('name', models.CharField(max_length=100, verbose_name='Имя пользователя')),
                ('username', models.CharField(max_length=50, null=True)),
                ('access', models.BooleanField(default=False, verbose_name='Доступ')),
            ],
            options={
                'verbose_name': 'Пользовател',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]