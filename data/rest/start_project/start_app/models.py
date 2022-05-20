
from ctypes import addressof
from unicodedata import name
from django.db import models
class User(models.Model):
    name = models.CharField(default = '', max_length=100, help_text='用户', verbose_name='用户名', unique = True)
    phone = models.CharField(default = '', max_length=100, help_text='手机号', verbose_name='手机号', unique = True)
    super_user = models.ForeignKey('User', default = None, blank=True, null= True, help_text='上级用户', verbose_name="上级用户", on_delete = models.PROTECT);
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = "user"
        verbose_name = "用户列表"

class Mechine(models.Model):
    pubkey = models.CharField(default = '', max_length=100, help_text='矿机公钥', verbose_name='矿机公钥', unique = True)
    pid = models.BigIntegerField(default = 0, help_text='pid', verbose_name='pid')
    v = models.BigIntegerField(default = 0, help_text='v', verbose_name='v')
    ve = models.BigIntegerField(default = 0, help_text='ve', verbose_name='ve')
    p_now = models.BigIntegerField(default = 0, help_text='当前得分', verbose_name='当前得分')
    p_init = models.BigIntegerField(default = 0, help_text='初始得分', verbose_name='初始得分')
    history_amount = models.FloatField(default = 0, help_text='历史总产量', verbose_name='历史总产量')
    stake_amount = models.FloatField(default = 0, help_text='质押金额', verbose_name='质押金额')
    status_now = models.CharField(default = '', max_length=100, help_text='当前状态', verbose_name='当前状态')
    start_time = models.BigIntegerField(default = 0, help_text='开始挖矿时间', verbose_name='开始挖矿时间')
    update_time = models.CharField(default = '', max_length=100, help_text='更新时间', verbose_name='更新时间')
    def __str__(self) -> str:
        return self.pubkey
    class Meta:
        db_table = "mechine"
        verbose_name = "机器列表"
        
class Pool(models.Model):
    pid = models.BigIntegerField(default = 0, help_text='pid', verbose_name='pid')
    owner = models.CharField(default = '', max_length=100, help_text='拥有者', verbose_name='拥有者')
    commission = models.FloatField(default = 0, help_text='佣金', verbose_name='佣金')
    cap = models.FloatField(default = 0, help_text='池子容量', verbose_name='池子容量')
    total_stake = models.FloatField(default = 0, help_text='total_stake', verbose_name='total_stake')
    free_stake = models.FloatField(default = 0, help_text='free_stake', verbose_name='free_stake')
    update_time = models.CharField(default = '', max_length=100, help_text='更新时间', verbose_name='更新时间')
    class Meta:
        db_table = "pool"
        verbose_name = "机器列表"
        
class DailyMeachine(models.Model):
    pubkey = models.CharField(default = '', max_length=100, help_text='矿机公钥', verbose_name='矿机公钥')
    amount = models.FloatField(default = 0, help_text='amount', verbose_name='amount')
    update_time = models.CharField(default = '', max_length=100, help_text='更新时间', verbose_name='更新时间')
    def __str__(self) -> str:
        return self.pubkey
    class Meta:
        db_table = "daily_mechine"
        verbose_name = "机器列表"
        
class Staker(models.Model):
    pid = models.BigIntegerField(default = 0, help_text='pid', verbose_name='pid')
    addr = models.CharField(default = '', max_length=100, help_text='addr', verbose_name='addr')
    locked = models.FloatField(default = 0, help_text='locked', verbose_name='locked')
    shares = models.BigIntegerField(default = 0, help_text='shares', verbose_name='shares')
    availableRewards = models.FloatField(default = 0, help_text='availableRewards', verbose_name='availableRewards')
    rewardDebt = models.FloatField(default = 0, help_text='rewardDebt', verbose_name='rewardDebt')
    update_time = models.CharField(default = '', max_length=100, help_text='更新时间', verbose_name='更新时间')
    class Meta:
        db_table = "staker"
        verbose_name = "质押列表"
        
class DailyOwnerUserCount(models.Model):
    day = models.CharField(default = '', max_length=100, help_text='记录时间', verbose_name='记录时间')
    count = models.FloatField(default = 0, help_text='count', verbose_name='count')
    update_time = models.CharField(default = '', max_length=100, help_text='更新时间', verbose_name='更新时间')
    class Meta:
        db_table = "daily_owner_user_count"
        verbose_name = "每日矿主数量"
        
class DailyStakeUserCount(models.Model):
    day = models.CharField(default = '', max_length=100, help_text='记录时间', verbose_name='记录时间')
    count = models.FloatField(default = 0, help_text='count', verbose_name='count')
    update_time = models.CharField(default = '', max_length=100, help_text='更新时间', verbose_name='更新时间')
    class Meta:
        db_table = "daily_stake_user_count"
        verbose_name = "每日投资者数量"
        
class DailyVCount(models.Model):
    day = models.CharField(default = '', max_length=100, help_text='记录时间', verbose_name='记录时间')
    count = models.FloatField(default = 0, help_text='count', verbose_name='count')
    update_time = models.CharField(default = '', max_length=100, help_text='更新时间', verbose_name='更新时间')
    class Meta:
        db_table = "daily_v_count"
        verbose_name = "每日V值数量"
        
class DailyStakeAmount(models.Model):
    day = models.CharField(default = '', max_length=100, help_text='记录时间', verbose_name='记录时间')
    all_amount = models.FloatField(default = 0, help_text='all_amount', verbose_name='all_amount')
    used_amount = models.FloatField(default = 0, help_text='used_amount', verbose_name='used_amount')
    update_time = models.CharField(default = '', max_length=100, help_text='更新时间', verbose_name='更新时间')
    class Meta:
        db_table = "daily_stake_amount"
        verbose_name = "质押列表"
        
class DailyMachinCount(models.Model):
    day = models.CharField(default = '', max_length=100, help_text='记录时间', verbose_name='记录时间')
    data = models.FloatField(default = 0, help_text='data', verbose_name='data')
    update_time = models.CharField(default = '', max_length=100, help_text='更新时间', verbose_name='更新时间')
    class Meta:
        db_table = "daily_mechine_count"
        verbose_name = "质押列表"
        
class DailyAllAmount(models.Model):
    day = models.CharField(default = '', max_length=100, help_text='记录时间', verbose_name='记录时间')
    amount = models.FloatField(default = 0, help_text='amount', verbose_name='amount')
    update_time = models.CharField(default = '', max_length=100, help_text='更新时间', verbose_name='更新时间')
    class Meta:
        db_table = "daily_all_amount"
        verbose_name = "质押列表"
        
class StatisticTop10Owner(models.Model):
    name = models.CharField(default = '', max_length=100, help_text='name', verbose_name='name')
    addr = models.CharField(default = '', max_length=100, help_text='addr', verbose_name='addr')
    v = models.FloatField(default = 0, help_text='v', verbose_name='v')
    percent = models.FloatField(default = 0, help_text='percent', verbose_name='percent')
    update_time = models.CharField(default = '', max_length=100, help_text='更新时间', verbose_name='更新时间')
    class Meta:
        db_table = "statistic_top10_owner"
        verbose_name = "top10矿主"
        
class StatisticTop10Staker(models.Model):
    name = models.CharField(default = '', max_length=100, help_text='name', verbose_name='name')
    addr = models.CharField(default = '', max_length=100, help_text='addr', verbose_name='addr')
    amount = models.FloatField(default = 0, help_text='v', verbose_name='v')
    percent = models.FloatField(default = 0, help_text='percent', verbose_name='percent')
    update_time = models.CharField(default = '', max_length=100, help_text='更新时间', verbose_name='更新时间')
    class Meta:
        db_table = "statistic_top10_staker"
        verbose_name = "top10质押者"
        
class LatestUpdate(models.Model):
    update_time = models.BigIntegerField(default = 0, help_text='LatestUpdate', verbose_name='LatestUpdate')
    class Meta:
        db_table = "latest_update"
        verbose_name = "最后更新时间"
"""
    select sum(locked)/1000000000000,sum(shares)/1000000000000 from staker ;
    select count(*) from (select * from staker where locked != 0 group by addr)as x;
"""