# Generated by Django 4.2.4 on 2023-08-12 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_userdetails_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviedetails',
            name='MovieID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
