# Generated by Django 3.1.5 on 2021-05-16 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20210514_1439'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-id']},
        ),
    ]
