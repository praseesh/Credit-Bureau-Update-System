# Generated by Django 5.1.3 on 2024-11-12 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit_bureau', '0004_remove_user_mobile_remove_user_name_user_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mobile',
            field=models.CharField(default='9999999999', max_length=15, unique=True),
        ),
    ]