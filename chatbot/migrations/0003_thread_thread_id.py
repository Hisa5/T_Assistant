# Generated by Django 3.2.25 on 2024-07-20 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='thread_id',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
