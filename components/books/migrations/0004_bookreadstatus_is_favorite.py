# Generated by Django 3.0.5 on 2020-04-12 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20200412_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookreadstatus',
            name='is_favorite',
            field=models.BooleanField(default=False),
        ),
    ]
