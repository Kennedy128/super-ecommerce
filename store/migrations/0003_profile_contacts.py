# Generated by Django 4.2.2 on 2023-06-17 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='contacts',
            field=models.CharField(default='SOME STRING', max_length=100),
        ),
    ]