# Generated by Django 3.0.7 on 2020-08-01 06:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200731_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.City'),
        ),
        migrations.AddField(
            model_name='post',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.Country'),
        ),
        migrations.AlterModelTable(
            name='post',
            table='blog_post',
        ),
    ]
