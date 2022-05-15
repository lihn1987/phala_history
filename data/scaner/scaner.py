import pymysql
import time
from urllib import request
import json
import sys
import signal
import threading

db = pymysql.connect("pha_mysql","root","123456","phala" )

def DealNum(num):
    if num == None:
        return 0
    elif num == "":
        return 0
    elif isinstance(num, str):
        return int(num, 16)
    else:
        return num

def GetStakerList():
    while True:
        try:
            res = request.urlopen('http://pha_node_api:3000/api/get_stake_list', timeout = 40)
            break
        except:
            print("time out")
    
    try:
        obj = json.loads(json.loads(res.read()))
        print(obj)
    except:
        exit(0)
    return obj
    
def GetStakerDetail(pid, addr):
    while True:
        try:
            res = request.urlopen('http://pha_node_api:3000/api/get_stake_detail?pid=%d&addr=%s'%(int(pid), addr), timeout = 20)
            break
        except:
            print("time out")
    
    try:
        obj = json.loads(json.loads(res.read()))
        # print(obj)
    except:
        exit(0)
    return obj

# 爬取所有质押者信息
def ClaimStaker():
    print("start claim staker")
    stake_list = GetStakerList()
    cursor = db.cursor()
    cursor.execute("delete from staker")
    for i, item in enumerate(stake_list):
        detail = GetStakerDetail(item["pid"], item["user"])
        print("claim stake %d/%d"%(i, len(stake_list)))
        pid = int(item["pid"])
        addr = item["user"]
        locked = detail["locked"] if not isinstance(detail["locked"], str) else int(detail["locked"], 16)
        shares = detail["shares"] if not isinstance(detail["shares"], str) else int(detail["shares"], 16)
        availableRewards = detail["availableRewards"] if not isinstance(detail["availableRewards"], str) else int(detail["availableRewards"], 16)
        rewardDebt = detail["rewardDebt"] if not isinstance(detail["rewardDebt"], str) else int(detail["rewardDebt"], 16)
        sql = """
            insert into staker(pid, addr, locked, shares, availableRewards, rewardDebt, update_time)
            values(
                %d,
                '%s',
                %d,
                %d,
                %d,
                %d,
                '%s'
            )
            """%(
                pid,
                addr,
                locked,
                shares,
                availableRewards,
                rewardDebt,
                time.time()
            )
        # print(sql)
        cursor.execute(sql)
    db.commit()
    
def GetPoolCount():
    while True:
        try:
            res = request.urlopen('http://pha_node_api:3000/api/get_pool_count', timeout = 20)
            break
        except:
            print("time out")
    res_obj = json.loads(json.loads(res.read()))
    return int(res_obj)

def GetOldAmount(pubkey):
    cursor = db.cursor()
    sql = "select history_amount from mechine where pubkey='%s'"%(pubkey);
    cursor.execute(sql)
    results = cursor.fetchall()
    old_amount = 0
    if len(results) != 0:
        old_amount = results[0][0]
    return old_amount

def ClaimWorkers():
    print("start claim worker")
    cursor = db.cursor()
    worker_list = []
    pool_count = GetPoolCount()

    sql = "delete from pool;"
    cursor.execute(sql)
    
    for i in range(pool_count):
        time_now = time.strftime("%Y-%m-%d", time.localtime())
        print("pid:%d/%d %0.2f%%"%(i, pool_count, i*100/pool_count))
        while True:
            try:
                res = request.urlopen('http://pha_node_api:3000/api/get_pool?pid=%d'%(i), timeout = 20)
                break
            except:
                pass
        miner_obj = json.loads(json.loads(res.read()))
        sql = """insert into pool(
                pid,
                owner,
                commission,
                cap,
                total_stake,
                free_stake,
                update_time
            )values(%d,'%s',%d,%d,%d,%d,%d)"""%(
                DealNum(miner_obj["pid"]),
                miner_obj["owner"],
                DealNum(miner_obj["payoutCommission"]),
                DealNum(miner_obj["cap"]),
                DealNum(miner_obj["totalStake"]),
                DealNum(miner_obj["freeStake"]),
                time.time()
                )
        # print(sql)
        cursor.execute(sql)
        for worker in miner_obj["workers"]:

            while True:
                try:
                    url = 'http://pha_node_api:3000/api/get_miner?pubkey=%s'%worker
                    res = request.urlopen(url, timeout = 20)
                    break
                except:
                    
                    print("time out")
                    
            obj = json.loads(json.loads(res.read()))
            
            # 记录当日收益
            sql = "select count(*) from daily_mechine where update_time = '%s' and pubkey='%s'"%(time_now, worker);
            cursor.execute(sql)
            results = cursor.fetchall()
            old_amount = GetOldAmount(worker)
            if results[0][0] == 0:
                sql = "insert into daily_mechine(pubkey, amount, update_time)values ('%s', %d ,'%s')"%(worker,DealNum(obj["stats"]["totalReward"])-old_amount,time_now);
                cursor.execute(sql)
            else:
                sql = "update daily_mechine set amount = amount+%d"%(DealNum(obj["stats"]["totalReward"])-old_amount)
                cursor.execute(sql)
            
            # print(obj["stats"]["totalReward"]/1000000000000)
            
            sql = "select count(*) from mechine where pubkey='%s'"%worker
            cursor.execute(sql)
            results = cursor.fetchall()
            same_count = results[0][0]
            if same_count == 0:
                sql = """
                insert into mechine(
                    pubkey,
                    pid,
                    v,
                    ve,
                    p_now,
                    p_init,
                    history_amount,
                    stake_amount,
                    status_now,
                    start_time,
                    update_time
                )values(
                    '%s',
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    %d,
                    '%s',
                    %d,
                    %d
                )
                """%(
                    worker,
                    i,
                    0 if obj["v"] == 0 else int(obj["v"][:18], 16),
                    0 if obj["v"] == 0 else int(obj["ve"][:18], 16),
                    DealNum(obj["benchmark"]["pInstant"]),
                    DealNum(obj["benchmark"]["pInit"]),
                    DealNum(obj["stats"]["totalReward"]),
                    0,
                    obj["state"],
                    DealNum(obj["benchmark"]["miningStartTime"]),
                    time.time()
                )
                cursor.execute(sql)
            else:
                sql = """
                update mechine
                    set 
                    pubkey = '%s',
                    pid = %d,
                    v = %d,
                    ve = %d,
                    p_now = %d,
                    p_init = %d,
                    history_amount = %d,
                    status_now = '%s',
                    start_time = %d,
                    update_time = %d
                where pubkey = '%s'
                """%(
                    worker,
                    i,
                    0 if obj["v"] == 0 else int(obj["v"][:18], 16),
                    0 if obj["v"] == 0 else int(obj["ve"][:18], 16),
                    DealNum(obj["benchmark"]["pInstant"]),
                    DealNum(obj["benchmark"]["pInit"]),
                    DealNum(obj["stats"]["totalReward"]),
                    obj["state"],
                    DealNum(obj["benchmark"]["miningStartTime"]),
                    time.time(),
                    worker
                )
                cursor.execute(sql)
        db.commit()
        
def ClaimWorkerStake():
    cursor = db.cursor()
    sql = "select id, pubkey from mechine where status_now='MiningIdle'";
    cursor.execute(sql)
    all_mechine = cursor.fetchall()
    index = 0
    max_index = len(all_mechine)
    for mechine in all_mechine:
        print("claimworker %d/%d, %0.2f"%(index, max_index, index*100.0/max_index))
        index += 1
        id = int(mechine[0])
        pubkey = mechine[1]
        while True:
            try:
                res = request.urlopen('http://pha_node_api:3000/api/get_mechine_stake?pubkey=%s'%(pubkey), timeout = 20)
                break
            except:
                pass
        stake_str = res.read().decode("utf-8");
        stake_str = stake_str.replace("\"", "")
        stake_obj = float(int(stake_str))
        sql = "update mechine set stake_amount=%0.2f where id=%d"%(stake_obj,id)
        cursor.execute(sql)
        db.commit()

def UpdateStaking():
    print("start update staking")
    time_now = time.strftime("%Y-%m-%d", time.localtime())
    cursor = db.cursor()
    sql="select sum(locked) from staker"
    cursor.execute(sql)
    all_stake = cursor.fetchall()[0][0]
    
    sql="select sum(stake_amount) from mechine"
    cursor.execute(sql)
    used_stake = cursor.fetchall()[0][0]
    
    sql = "select count(*) from daily_stake_amount where day='%s'"%time_now
    cursor.execute(sql)
    exist = cursor.fetchall()[0][0]
    if exist == 0:
        sql = """
        insert into 
        daily_stake_amount(
            day,
            all_amount,
            used_amount,
            update_time
        ) values(
            '%s',
            %0.2f,
            %0.2f,
            %d
        )
        """%(time_now, float(all_stake), float(used_stake), time.time())
        cursor.execute(sql)
        print("not exist")
    else:
        sql = """
        update 
            daily_stake_amount 
        set 
            all_amount=%0.2f,
            used_amount=%0.2f,
            update_time=%d
        where
            day='%s'
        """%(float(all_stake), float(used_stake), time.time(),time_now)
        cursor.execute(sql)
    db.commit()


if __name__ == "__main__":
    while True:
        ClaimStaker()
        ClaimWorkerStake()
        ClaimWorkers()
        UpdateStaking()