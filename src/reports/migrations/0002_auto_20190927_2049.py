# Generated by Django 2.2 on 2019-09-27 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ('-timestamp',)},
        ),
    ]
