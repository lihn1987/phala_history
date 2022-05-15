# Generated by Django 4.0.4 on 2022-05-09 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('start_app', '0008_dailymachincount_dailystakeamount_dailyusercount'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyMeachine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pubkey', models.CharField(default='', help_text='矿机公钥', max_length=100, unique=True, verbose_name='矿机公钥')),
                ('amount', models.BigIntegerField(default=0, help_text='amount', verbose_name='amount')),
                ('update_time', models.CharField(default='', help_text='更新时间', max_length=100, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '机器列表',
                'db_table': 'daily_mechine',
            },
        ),
        migrations.AlterField(
            model_name='mechine',
            name='history_amount',
            field=models.BigIntegerField(default=0, help_text='历史总产量', verbose_name='历史总产量'),
        ),
        migrations.AlterField(
            model_name='mechine',
            name='p_init',
            field=models.BigIntegerField(default=0, help_text='初始得分', verbose_name='初始得分'),
        ),
        migrations.AlterField(
            model_name='mechine',
            name='p_now',
            field=models.BigIntegerField(default=0, help_text='当前得分', verbose_name='当前得分'),
        ),
        migrations.AlterField(
            model_name='mechine',
            name='stake_amount',
            field=models.BigIntegerField(default=0, help_text='质押金额', verbose_name='质押金额'),
        ),
        migrations.AlterField(
            model_name='mechine',
            name='status_now',
            field=models.BigIntegerField(default=0, help_text='当前状态', verbose_name='当前状态'),
        ),
        migrations.AlterField(
            model_name='mechine',
            name='v',
            field=models.BigIntegerField(default=0, help_text='v', verbose_name='v'),
        ),
        migrations.AlterField(
            model_name='mechine',
            name='ve',
            field=models.BigIntegerField(default=0, help_text='ve', verbose_name='ve'),
        ),
    ]
