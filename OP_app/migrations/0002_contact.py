# Generated by Django 4.1.1 on 2022-09-25 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OP_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField(max_length=500)),
            ],
        ),
    ]
