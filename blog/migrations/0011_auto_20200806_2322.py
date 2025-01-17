# Generated by Django 3.0.7 on 2020-08-07 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='phonecode',
            field=models.IntegerField(default=True),
        ),
        migrations.AddField(
            model_name='country',
            name='sortname',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
