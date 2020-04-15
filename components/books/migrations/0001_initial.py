# Generated by Django 3.0.5 on 2020-04-15 02:57

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('image', models.URLField()),
                ('paperback', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'book',
            },
        ),
        migrations.CreateModel(
            name='BookCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'book_category',
            },
        ),
        migrations.CreateModel(
            name='BookReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('messages', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=512), size=None), size=None)),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='books.Book')),
            ],
            options={
                'db_table': 'book_review',
            },
        ),
        migrations.CreateModel(
            name='BookRequestBuy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_url', models.URLField()),
                ('name', models.CharField(max_length=256)),
                ('price', models.IntegerField(default=1)),
                ('status', models.IntegerField(choices=[(1, 'waiting'), (2, 'approved'), (3, 'bought'), (4, 'reject')], default=1)),
                ('book_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.BookCategory')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'book_request_buy',
            },
        ),
        migrations.CreateModel(
            name='BookReadStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('0', 'unread'), ('1', 'reading'), ('2', 'read')], default='0', max_length=56)),
                ('page_reading', models.IntegerField(default=0)),
                ('is_favorite', models.BooleanField(default=False)),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='books.Book')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'book_read_status',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='book_category',
            field=models.ManyToManyField(to='books.BookCategory'),
        ),
    ]
