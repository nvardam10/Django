# Generated by Django 4.2.4 on 2023-08-12 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_alter_moviebooking_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='email_id',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]