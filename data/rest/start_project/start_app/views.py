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
