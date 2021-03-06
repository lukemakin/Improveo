# Generated by Django 2.2 on 2019-09-25 22:55

import django.core.validators
from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20190925_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=posts.models.get_upload_path, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])]),
        ),
    ]
