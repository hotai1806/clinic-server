# Generated by Django 4.0.3 on 2022-05-21 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.TextField(blank=True, null=True),
        ),
    ]
