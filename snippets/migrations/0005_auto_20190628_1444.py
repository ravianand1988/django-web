# Generated by Django 2.2.1 on 2019-06-28 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0004_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='username',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
