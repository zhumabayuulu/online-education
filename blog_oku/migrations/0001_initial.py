# Generated by Django 4.0.6 on 2024-02-07 09:09

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogLearn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='BlogLearnComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=150)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('bloglearn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog_oku.bloglearn')),
                ('liked', models.ManyToManyField(blank=True, default=None, related_name='like_learn', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='LearnCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ObjectCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='TestCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('maximum_attemps', models.PositiveIntegerField()),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(default=datetime.datetime(2024, 2, 17, 9, 9, 44, 285388, tzinfo=utc))),
                ('pass_percentage', models.PositiveIntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_oku.testcategory')),
                ('liked', models.ManyToManyField(blank=True, default=None, related_name='like_test', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=333)),
                ('a', models.CharField(max_length=151)),
                ('b', models.CharField(max_length=151)),
                ('c', models.CharField(max_length=151)),
                ('d', models.CharField(max_length=151)),
                ('true_answer', models.CharField(help_text='E.x:a', max_length=151)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_oku.test')),
            ],
        ),
        migrations.CreateModel(
            name='LikeTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(choices=[('Like', 'Like'), ('Unlike', 'Unlike')], default='like', max_length=10)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_oku.test')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LikeOku',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(choices=[('Like', 'Like'), ('Unlike', 'Unlike')], default='like', max_length=10)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_oku.bloglearn')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LikeLearn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(choices=[('Like', 'Like'), ('Unlike', 'Unlike')], default='like', max_length=10)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_oku.bloglearncomment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CheckTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finded_questions', models.PositiveIntegerField(default=0)),
                ('user_passed', models.BooleanField(default=False)),
                ('percentage', models.PositiveIntegerField(default=0)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_oku.test')),
            ],
        ),
        migrations.CreateModel(
            name='CheckQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('given_answer', models.CharField(help_text='E.x:a', max_length=1)),
                ('true_answer', models.CharField(help_text='E.x:a', max_length=1)),
                ('is_true', models.BooleanField(default=False)),
                ('checktest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_oku.checktest')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_oku.question')),
            ],
        ),
        migrations.AddField(
            model_name='bloglearn',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_oku.learncategory'),
        ),
        migrations.AddField(
            model_name='bloglearn',
            name='liked',
            field=models.ManyToManyField(blank=True, default=None, related_name='like_oku', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bloglearn',
            name='object_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_oku.objectcategory'),
        ),
    ]
