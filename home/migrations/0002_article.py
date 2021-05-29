# Generated by Django 3.2 on 2021-05-04 07:17

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, upload_to='article/%Y%m%d/')),
                ('title', models.CharField(blank=True, max_length=20)),
                ('tags', models.CharField(blank=True, max_length=20)),
                ('summary', models.CharField(max_length=200, null=True)),
                ('content', models.TextField()),
                ('total_views', models.PositiveIntegerField(default=0)),
                ('total_comments', models.PositiveIntegerField(default=0)),
                ('created_time', models.DateTimeField(default=datetime.datetime(2021, 5, 4, 7, 17, 41, 812685, tzinfo=utc))),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='home.articlecategory')),
            ],
            options={
                'verbose_name': '文章管理',
                'verbose_name_plural': '文章管理',
                'db_table': 'tb_article',
                'ordering': ('-created_time', 'title'),
            },
        ),
    ]
