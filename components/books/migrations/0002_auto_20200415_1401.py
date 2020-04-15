# Generated by Django 3.0.5 on 2020-04-15 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.IntegerField(choices=[(0, 'VN'), (1, 'JP'), (2, 'EN')], default=0),
        ),
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='bookreadstatus',
            name='status',
            field=models.IntegerField(choices=[(0, 'unread'), (1, 'reading'), (2, 'read')], default=0),
        ),
    ]