# Generated by Django 4.1.7 on 2023-04-12 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0018_alter_familymember_family_choice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actor',
            name='family_member',
        ),
    ]
