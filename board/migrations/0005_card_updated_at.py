# Generated by Django 4.2.11 on 2024-05-08 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("board", "0004_column_updated_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="card",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
