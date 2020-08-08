# Generated by Django 3.0.7 on 2020-08-07 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_country'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='country',
            table='all_country',
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Country')),
            ],
        ),
    ]