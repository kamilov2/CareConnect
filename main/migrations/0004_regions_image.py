# Generated by Django 4.2.11 on 2024-05-14 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_alter_news_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="regions",
            name="image",
            field=models.ImageField(default=0, upload_to="regions_images/"),
            preserve_default=False,
        ),
    ]