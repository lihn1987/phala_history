# Generated by Django 4.0.4 on 2022-04-27 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('start_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户'},
        ),
        migrations.AlterField(
            model_name='user',
            name='super_user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='start_app.user'),
        ),
    ]
