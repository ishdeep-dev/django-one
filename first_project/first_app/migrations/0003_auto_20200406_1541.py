# Generated by Django 3.0.3 on 2020-04-06 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_formdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formdata',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
