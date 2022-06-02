from django.shortcuts import render

import os
import json
import time
import hashlib
import random
from urllib import request as Request
from django.db import connection
from django.http import  JsonResponse

def get_top10_owner(request):
    if request.method == 'GET':
        cursor = connection.cursor()
        sql= "select name, addr, v, percent from statistic_top10_owner order by id"
        cursor.execute(sql)
        res_all = cursor.fetchall()
        print(res_all)
        rtn = {
            "result": 0,
            "data": []
        }
        for item in res_all:
            rtn["data"].append({
                "name": item[0],
                "addr": item[1],
                "v": item[2],
                "percent": item[3],
            })
        return JsonResponse(rtn)
    
def get_top10_staker(request):
    if request.method == 'GET':
        cursor = connection.cursor()
        sql= "select name, addr, amount, percent from statistic_top10_staker order by id"
        cursor.execute(sql)
        res_all = cursor.fetchall()
        print(res_all)
        rtn = {
            "result": 0,
            "data": []
        }
        for item in res_all:
            rtn["data"].append({
                "name": item[0],
                "addr": item[1],
                "amount": item[2],
                "percent": item[3],
            })
        return JsonResponse(rtn)
    
def get_param(request):
    if request.method == 'GET':
        
        cursor = connection.cursor()
        sql= "select data from daily_mechine_count order by day desc limit 1"
        cursor.execute(sql)
        all_mechines_count = cursor.fetchall()[0][0]
        
        sql= "select count from daily_v_count order by day desc limit 1"
        cursor.execute(sql)
        all_v = cursor.fetchall()[0][0]
        
        sql= "select all_amount,used_amount from daily_stake_amount order by day desc limit 1"
        cursor.execute(sql)
        res = cursor.fetchall()
        all_stake_amount = res[0][0]
        all_right_stake_amount = res[0][1]
        
        sql= "select count from daily_owner_user_count order by day desc limit 1"
        cursor.execute(sql)
        all_owner_count = cursor.fetchall()[0][0]
        
        sql= "select count from daily_stake_user_count order by day desc limit 1"
        cursor.execute(sql)
        all_staker_count = cursor.fetchall()[0][0]
        
        rtn = {
            "result": 0,
            "data":{
                "all_mechines_count":all_mechines_count,
                "all_v":all_v,
                "all_stake_amount":all_stake_amount,
                "all_right_stake_amount":all_right_stake_amount,
                "all_owner_count":all_owner_count,
                "all_staker_count":all_staker_count,
            }
        }
        return JsonResponse(rtn)

def get_latest_daily_v(request): 
    if request.method == 'GET':
        cursor = connection.cursor()
        sql= "select day,count from daily_v_count order by day limit 30;"
        cursor.execute(sql)
        all_item = cursor.fetchall()
        rtn = {
            "result": 0,
            "data":{
                "label_data":[],
                "value_data":[]
            }
        }
        for item in all_item:
            rtn["data"]["label_data"].append(item[0])
            rtn["data"]["value_data"].append(item[1])
        return JsonResponse(rtn)

def get_latest_daily_stake(request): 
    if request.method == 'GET':
        cursor = connection.cursor()
        sql= "select day, all_amount, used_amount from daily_stake_amount order by day limit 30;"
        cursor.execute(sql)
        all_item = cursor.fetchall()
        rtn = {
            "result": 0,
            "data":{
                "label_data":[],
                "value_data1":[],
                "value_data2":[]
            }
        }
        for item in all_item:
            rtn["data"]["label_data"].append(item[0])
            rtn["data"]["value_data1"].append(item[1])
            rtn["data"]["value_data2"].append(item[2])
        return JsonResponse(rtn)

def get_latest_daily_mechine_count(request): 
    if request.method == 'GET':
        cursor = connection.cursor()
        sql= "select day,data from daily_mechine_count order by day limit 30;"
        cursor.execute(sql)
        all_item = cursor.fetchall()
        rtn = {
            "result": 0,
            "data":{
                "label_data":[],
                "value_data":[]
            }
        }
        for item in all_item:
            rtn["data"]["label_data"].append(item[0])
            rtn["data"]["value_data"].append(item[1])
        return JsonResponse(rtn)

def get_latest_daily_mechine_user_count(request): 
    if request.method == 'GET':
        cursor = connection.cursor()
        sql= "select day,count from daily_owner_user_count order by day limit 30;"
        cursor.execute(sql)
        all_item = cursor.fetchall()
        rtn = {
            "result": 0,
            "data":{
                "label_data":[],
                "value_data":[]
            }
        }
        for item in all_item:
            rtn["data"]["label_data"].append(item[0])
            rtn["data"]["value_data"].append(item[1])
        return JsonResponse(rtn)

def get_mechines(request, pid, status, pubkey, page): #
    if request.method == 'GET':
        cursor = connection.cursor()
        print(pid, status, pubkey)
        where_sql = ""
        if pid != "-":
            where_sql = where_sql + (" where pid = %s "%pid if where_sql == "" else "and pid = %s "%pid)
        if status != "-":
            if status == "0":
                where_sql = where_sql + (" where status_now = 'MiningIdle' " if where_sql == "" else " and status_now = 'MiningIdle' ")
            elif status == "1":
                where_sql = where_sql + (" where status_now != 'MiningIdle' and status_now != 'Ready' " if where_sql == "" else " and status_now != 'MiningIdle' and status_now != 'Ready' ")
            elif status == "2":
                where_sql = where_sql + (" where status_now != 'MiningIdle' and status_now != 'Ready' and status_now !='MiningCoolingDown' " if where_sql == "" else " and status_now != 'MiningIdle' and status_now != 'Ready' and status_now !='MiningCoolingDown' ")
        if pubkey != "-":
            where_sql = where_sql + (" where pubkey = '%s' "%pubkey if where_sql == "" else "and pubkey = '%s' "%pubkey)

        sql = """
            select 
                count(*)
            from 
                mechine 
            %s
            order by id
        """%where_sql
        cursor.execute(sql)
        res = cursor.fetchall()
        all_count = res[0][0]
        sql= """
            select 
                name,
                pubkey,
                v,
                p_init,
                history_amount, 
                stake_amount, 
                status_now, 
                update_time, 
                pid,
                start_time,
                update_time 
            from 
                mechine 
            %s
            order by id 
            limit %d,10"""%( where_sql,page*10)
        cursor.execute(sql)
        all_item = cursor.fetchall()
        rtn = {
            "result": 0,
            "count":all_count,
            "data":[]
        }
        for item in all_item:
            rtn["data"].append(
                {
                "name": item[0],
                "pubkey": item[1],
                "v": item[2],
                "p_init": item[3],
                "history_amount": item[4] ,
                "stake_amount": item[5] ,
                "status_now": item[6] ,
                "update_time": item[7] ,
                "pid": item[8],
                "start_time": item[9],
                "update_time": item[10]
                }
            )
        return JsonResponse(rtn)

def get_bml_error_pid(request):
    if request.method == 'GET':
        cursor = connection.cursor()
        sql= """
        select pid from pool where 
        ((pid >= 413 and 
        pid <= 476) or 
        pid in (1922,1923,1924,1925,1926,1934)) and 
        with_draw_queue = 1
        """
        cursor.execute(sql)
        all_item = cursor.fetchall()
        rtn = {
            "result": 0,
            "data":[]
        }
        for item in all_item:
            rtn["data"].append(item[0])
        return JsonResponse(rtn)

def get_bml_special_error_mechine(request):
    if request.method == 'GET':
        cursor = connection.cursor()
        sql = """
        select 
            name,
            pubkey,
            v,
            p_init,
            history_amount, 
            stake_amount, 
            status_now, 
            pid,
            start_time,
            update_time 
        from 
            mechine 
        where 
            status_now != "MiningIdle" AND
            status_now != "Ready" and 
            pid in (422, 424, 451, 453 ,455 ,457)
        order by id 
        """
        cursor.execute(sql)
        all_item = cursor.fetchall()
        rtn = {
            "result": 0,
            "data":[]
        }
        for item in all_item:
            rtn["data"].append(
                {
                "name": item[0],
                "pubkey": item[1],
                "v": item[2],
                "p_init": item[3],
                "history_amount": item[4] ,
                "stake_amount": item[5] ,
                "status_now": item[6] ,
                "pid": item[7],
                "start_time": item[8],
                "update_time": item[9]
                }
            )
        return JsonResponse(rtn)

def get_bml_error_mechine(request):
    if request.method == 'GET':
        cursor = connection.cursor()
        sql = """
        select 
            name,
            pubkey,
            v,
            p_init,
            history_amount, 
            stake_amount, 
            status_now, 
            pid,
            start_time,
            update_time 
        from 
            mechine 
        where 
            status_now != "MiningIdle" AND
            status_now != "Ready" and 
            status_now != 'MiningCoolingDown' and
            ((pid >= 413 and 
            pid <= 476) or 
            pid in (1922,1923,1924,1925,1926,1934))
        order by id 
        """
        cursor.execute(sql)
        all_item = cursor.fetchall()
        rtn = {
            "result": 0,
            "data":[]
        }
        for item in all_item:
            rtn["data"].append(
                {
                "name": item[0],
                "pubkey": item[1],
                "v": item[2],
                "p_init": item[3],
                "history_amount": item[4] ,
                "stake_amount": item[5] ,
                "status_now": item[6] ,
                "pid": item[7],
                "start_time": item[8],
                "update_time": item[9]
                }
            )
        return JsonResponse(rtn)