# Generated by Django 4.0.1 on 2022-02-08 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_rename_long_businessdetail_lng_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessdetail',
            name='identity_proof',
            field=models.FileField(upload_to='media'),
        ),
    ]
