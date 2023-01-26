# Generated by Django 4.1.1 on 2023-01-21 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OP_app', '0013_order_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('First_name', models.CharField(max_length=15)),
                ('Last_name', models.CharField(max_length=15)),
                ('Adress', models.CharField(max_length=500)),
                ('State', models.CharField(max_length=200)),
                ('Posta', models.BigIntegerField(max_length=6)),
                ('Email', models.EmailField(max_length=254)),
                ('mobile_no', models.BigIntegerField(max_length=10)),
            ],
        ),
    ]
