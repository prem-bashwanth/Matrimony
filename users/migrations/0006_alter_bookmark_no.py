# Generated by Django 4.2.4 on 2023-10-28 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_bookmark_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='no',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
