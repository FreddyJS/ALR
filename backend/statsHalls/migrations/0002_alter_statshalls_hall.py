# Generated by Django 4.0.2 on 2022-04-19 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statsHalls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statshalls',
            name='hall',
            field=models.TextField(unique=True),
        ),
    ]
