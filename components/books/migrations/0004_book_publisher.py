# Generated by Django 3.0.5 on 2020-04-15 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20200415_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
