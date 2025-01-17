# Generated by Django 3.0.7 on 2010-02-25 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_auto_20200806_2328'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sortname', models.CharField(max_length=200, null=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('phonecode', models.IntegerField(default=True)),
            ],
            options={
                'db_table': 'blog_country',
            },
        ),
        migrations.RenameField(
            model_name='city',
            old_name='country',
            new_name='state',
        ),
        migrations.AddField(
            model_name='post',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.Country'),
        ),
        migrations.AddField(
            model_name='state',
            name='country',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Country'),
            preserve_default=False,
        ),
    ]
