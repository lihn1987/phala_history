import pymysql
import time
from urllib import request,parse
import json
import binascii

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
    obj = None
    while True:
        try:
            res = request.urlopen('http://pha_node_api:3000/api/get_stake_list', timeout = 50)
            obj = json.loads(json.loads(res.read()))
            break
        except:
            print("time out")
            time.sleep(1)

        

    return obj
    
def GetStakerDetail(pid, addr):
    res = None
    while True:
        try:
            res = request.urlopen('http://pha_node_api:3000/api/get_stake_detail?pid=%d&addr=%s'%(int(pid), addr), timeout = 20)
            obj = json.loads(json.loads(res.read()))
            break
        except:
            print("time out")
            time.sleep(1)
    return obj

def GetStakerDetails(stake_list):
    obj = None
    while True:
        try:
            # res = request.urlopen('http://pha_node_api:3000/api/get_pools', data=bytes(json.dumps({"pids":pids}), encoding="utf8"), timeout=20,timeout = 10)
            args = []
            for item in stake_list:
                args.append((int(item['pid']), item['user']))
            print("start detail")
            res = request.urlopen('http://pha_node_api:3000/api/get_stake_details', data=bytes(json.dumps({"pid_addr":args}), encoding="utf8"), timeout=20)
            obj = json.loads(res.read())
            # print(res.read())
            break
        except:
            print("time out")
            time.sleep(1)
    
    try:
        rtn = []
        
        for item_str in obj:
            item = json.loads(item_str)
            rtn.append(item)
    except:
        print("json_load error")
        time.sleep(1)
    return rtn

# 爬取所有质押者信息
def ClaimStaker():
    print("start claim staker")
    stake_list = GetStakerList()
    details = GetStakerDetails(stake_list)
    
    cursor = db.cursor()
    sql="delete from staker"
    cursor.execute(sql)
    for i, item in enumerate(stake_list):
        detail = details[i]
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
    res_obj = None
    while True:
        try:
            res = request.urlopen('http://pha_node_api:3000/api/get_pool_count', timeout=20)
            res_obj = json.loads(json.loads(res.read()))
            break
        except:
            time.sleep(1)
            print("time out")
    
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
    pubkey2pid={}
    worker_list = []
    pid_list = []
    pool_count = GetPoolCount()
    
    for i in range(int((pool_count-1)/100)+1):
        print("stake %d/%d"%(i, int((pool_count-1)/100)))
        pids = []
        res_list = None
        for index in range(int(i*100), int((i+1)*100) if int((i+1)*100) < pool_count else pool_count):
            pids.append(index)
        while True:
            try:
                res = request.urlopen('http://pha_node_api:3000/api/get_pools', data=bytes(json.dumps({"pids": pids}), encoding="utf8"), timeout=20)
                res_list = json.loads(res.read())
                break
            except:
                print("time_out")
                time.sleep(1)
        
        for item_str in res_list:
            pid_list.append(json.loads(item_str))
            
            
            
            
    print("start claim pid")
    for pid_obj in pid_list:
        i = pid_obj["pid"]
        time_now = time.strftime("%Y-%m-%d", time.localtime())
        sql = "select count(*) from pool where pid=%d"%i
        cursor.execute(sql)
        exist = int(cursor.fetchall()[0][0])
        miner_obj = pid_obj
        worker_list.extend(miner_obj["workers"])
        for item in miner_obj["workers"]:
            pubkey2pid[item] = i
        if exist == 0:
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
        else:
            sql = """update pool
                    set owner = '%s',
                    commission = %d,
                    cap = %d,
                    total_stake = %d,
                    free_stake = %d,
                    update_time = %d
                where pid=%d"""%(
                    miner_obj["owner"],
                    DealNum(miner_obj["payoutCommission"]),
                    DealNum(miner_obj["cap"]),
                    DealNum(miner_obj["totalStake"]),
                    DealNum(miner_obj["freeStake"]),
                    time.time(),
                    DealNum(miner_obj["pid"])
                    )
            cursor.execute(sql)
    db.commit()
    print("start claim workers address", len(worker_list))
    address_list = []
    # res = request.urlopen('http://pha_node_api:3000/api/pubkey_2_address', data=bytes(json.dumps({"pubkeys": worker_ags}), encoding="utf8"), timeout=20, timeout = 50)
    for i in range(int((len(worker_list)-1)/100)+1):
        print("claim pid %d/%d"%(i, int((len(worker_list)-1)/100)))
        worker_ags = []
        for worker in worker_list[int(i*100): int((i+1)*100) if int((i+1)*100) < len(worker_list) else len(worker_list)]:
            worker_ags.append(worker)
            
        res_list = None
        while True:
            try:
                res = request.urlopen('http://pha_node_api:3000/api/pubkey_2_address', data=bytes(json.dumps({"pubkeys": worker_ags}), encoding="utf8"), timeout=20)
                res_list = json.loads(res.read())
                break
            except:
                print("time_out")
                time.sleep(1)
                
        
        for addr in res_list:
            address_list.append(addr)
            
            
    stakes = []
    print("start claim stakes")
    for i in range(int((len(address_list)-1)/1000)+1):
        addr_args = []
        for address in address_list[int(i*1000): int((i+1)*1000) if int((i+1)*1000) < len(address_list) else len(address_list)]:
            addr_args.append(address)
            
        res_list = None
        while True:
            try:
                res = request.urlopen('http://pha_node_api:3000/api/get_mechines_stake', data=bytes(json.dumps({"addrs": addr_args}), encoding="utf8"), timeout=20)
                res_list = json.loads(res.read())
                break
            except:
                print("time_out")
                time.sleep(1)
                
        
        for stake in res_list:
            stakes.append(0 if stake=='' else int(stake,10))
            
    
    print("start claim workers details", len(address_list))
    details = []
    for i in range(int((len(address_list)-1)/100)+1):
        print("%d/%d"%(i,int((len(address_list)-1)/100)+1))
        addr_args = []
        for addr in address_list[int(i*100): int((i+1)*100) if int((i+1)*100) < len(address_list) else len(address_list)]:
            addr_args.append(addr)
        obj = None
        while True:
            try:
                res = request.urlopen('http://pha_node_api:3000/api/get_miner_details', data=bytes(json.dumps({"addrs": addr_args}), encoding="utf8"), timeout=20)
                obj = json.loads(res.read())
                break
            except:
                print("time_out")
                time.sleep(1)
        for item in obj:
            try:
                details.append(json.loads(item))
            except:
                print("!!!!!->", item)
                time.sleep(1)
                exit(0)
            
    for i, worker in enumerate(worker_list) :
        print(len(worker_list),i)
        obj = details[i]
        
        # 记录当日收益
        sql = "select count(*) from daily_mechine where update_time = '%s' and pubkey='%s'"%(time_now, worker);
        cursor.execute(sql)
        results = cursor.fetchall()
        old_amount = GetOldAmount(worker)
        if results[0][0] == 0:
            sql = "insert into daily_mechine(pubkey, amount, update_time)values ('%s', %d ,'%s')"%(worker,DealNum(obj["stats"]["totalReward"])-old_amount,time_now);
            cursor.execute(sql)
        else:
            sql = "update daily_mechine set amount = amount+%d where pubkey = '%s'"%(DealNum(obj["stats"]["totalReward"])-old_amount, worker)
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
                pubkey2pid[worker],
                0 if obj["v"] == 0 else int(obj["v"][:18], 16),
                0 if obj["v"] == 0 else int(obj["ve"][:18], 16),
                DealNum(obj["benchmark"]["pInstant"]),
                DealNum(obj["benchmark"]["pInit"]),
                DealNum(obj["stats"]["totalReward"]),
                stakes[i],
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
                update_time = %d,
                stake_amount = %d
            where pubkey = '%s'
            """%(
                worker,
                pubkey2pid[worker],
                0 if obj["v"] == 0 else int(obj["v"][:18], 16),
                0 if obj["v"] == 0 else int(obj["ve"][:18], 16),
                DealNum(obj["benchmark"]["pInstant"]),
                DealNum(obj["benchmark"]["pInit"]),
                DealNum(obj["stats"]["totalReward"]),
                obj["state"],
                DealNum(obj["benchmark"]["miningStartTime"]),
                time.time(),
                stakes[i],
                worker
            )
            cursor.execute(sql)
            db.commit()
        


def UpdateStaking():
    print("start update staking")
    time_now = time.strftime("%Y-%m-%d", time.localtime())
    cursor = db.cursor()
    
    # 计算所有质押与有效质押
    sql="select sum(locked) from staker"
    cursor.execute(sql)
    all_stake = cursor.fetchall()[0][0]
    
    sql="select sum(stake_amount) from mechine where status_now='MiningIdle'"
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
    # 计算有效质押人数
    sql = """
    select count(*) 
    from (
        select 
        addr
        from staker,
        (
            select 
                pid 
            from 
                mechine 
            where 
                status_now = 'MiningIdle' 
            group by pid
        ) as x
    where staker.pid = x.pid and staker.locked != 0
    group by addr) as y
    """
    cursor.execute(sql)
    staka_user_count = cursor.fetchall()[0][0]
    
    sql = "select count(*) from daily_stake_user_count where day='%s'"%time_now
    cursor.execute(sql)
    exist = cursor.fetchall()[0][0]

    if exist == 0:
        sql = """
        insert into 
        daily_stake_user_count(
            day,
            count,
            update_time
        ) values(
            '%s',
            %0.2f,
            %d
        )
        """%(time_now, float(staka_user_count), time.time())
        cursor.execute(sql)
        print("not exist")
    else:
        sql = """
        update 
            daily_stake_user_count
        set 
            count=%0.2f,
            update_time=%d
        where
            day='%s'
        """%(float(staka_user_count), time.time(),time_now)
        cursor.execute(sql)
        
        
    db.commit()

def UpdateMechinCount():
    print("start update mechine_count")
    time_now = time.strftime("%Y-%m-%d", time.localtime())
    cursor = db.cursor()
    
    # 填充机器数量
    sql = "select count(*) from mechine where status_now = 'MiningIdle'"
    cursor.execute(sql)
    mechine_count = int(cursor.fetchall()[0][0])
    sql = "select count(*) from daily_mechine_count where day='%s'"%time_now
    cursor.execute(sql)
    exist = cursor.fetchall()[0][0]
    if int(exist) == 0:
        sql = "insert into daily_mechine_count(day,data,update_time) values('%s', %0.2f, %d)"%(time_now, mechine_count, time.time())
        cursor.execute(sql)
    else:
        sql = "update daily_mechine_count set data = %0.2f,update_time=%d where day = '%s'"%(mechine_count, time.time(), time_now)
        cursor.execute(sql)
        
    # 填充机器v值
    sql = "select sum(v) from mechine where status_now = 'MiningIdle'"
    cursor.execute(sql)
    v_count = int(cursor.fetchall()[0][0])
    sql = "select count(*) from daily_v_count where day='%s'"%time_now
    cursor.execute(sql)
    exist = cursor.fetchall()[0][0]
    if int(exist) == 0:
        sql = "insert into daily_v_count(day,count,update_time) values('%s', %0.2f, %d)"%(time_now, v_count, time.time())
        cursor.execute(sql)
    else:
        sql = "update daily_v_count set count = %0.2f,update_time=%d where day = '%s'"%(v_count, time.time(), time_now)
        cursor.execute(sql)
        
    # 更新机器主数量
    sql = """
    select count(*) from (
    select 
    pool.`owner`
    from 
    mechine,pool
    where 
        mechine.pid = pool.pid and
        mechine.status_now='MiningIdle'
    group by pool.`owner`
    ) as x
    """
    cursor.execute(sql)
    owner_count = int(cursor.fetchall()[0][0])
    sql = "select count(*) from daily_owner_user_count where day='%s'"%time_now
    cursor.execute(sql)
    exist = cursor.fetchall()[0][0]
    if int(exist) == 0:
        sql = "insert into daily_owner_user_count(day,count,update_time) values('%s', %0.2f, %d)"%(time_now, owner_count, time.time())
        cursor.execute(sql)
    else:
        sql = "update daily_owner_user_count set count = %0.2f,update_time=%d where day = '%s'"%(owner_count, time.time(), time_now)
        cursor.execute(sql)
    db.commit()
    
def GetAccountName(addrs):
    rtns = []
    while True:
        try:
            res = request.urlopen('http://pha_node_api:3000/api/get_accounts_name', data=bytes(json.dumps({"addrs":addrs}), encoding="utf8"), timeout=20)
            str = res.read().decode("utf-8");
            list = json.loads(str)
            for item_str in list:
                if item_str == '':
                    rtns.append('')
                else:
                    item = json.loads(item_str)
                    raw = item["info"]["display"]["raw"]
                    s = binascii.unhexlify(raw.replace("0x", ""))
                    rtns.append(s.decode("utf-8"))
            break
        except:
            print("error")
            time.sleep(0)
    return rtns

# 计算今日产量
def StatisticTodayAmount():
    print("start static today amount")
    cursor = db.cursor()
    time_now = time.strftime("%Y-%m-%d", time.localtime())
    
    sql = "select sum(amount) from daily_mechine where update_time = '%s'"%time_now
    cursor.execute(sql)
    today_amount = cursor.fetchall()[0][0]

    sql = "select count(*) from daily_all_amount where day='%s'"%time_now
    cursor.execute(sql)
    if cursor.fetchall()[0][0] == 0:
        sql = "insert into daily_all_amount(day, amount, update_time) values('%s', %02f, %d)"%(time_now, today_amount, time.time())
        cursor.execute(sql)
    else:
        sql = "update daily_all_amount set  amount=%02f, update_time=%d where day='%s'"%(today_amount, time.time(), time_now)
        cursor.execute(sql)
    # sql = "select sum(amount) from daily_mechine where update_time = '%s'"
    db.commit()
    
def StatisticTop10Owner():
    print("start statistic top10 owner")
    cursor = db.cursor()
    time_now = time.strftime("%Y-%m-%d", time.localtime())
    sql = "delete from  statistic_top10_owner"
    cursor.execute(sql)
    sql = "select sum(v) from mechine where status_now='MiningIdle'"
    cursor.execute(sql)
    all_v = float(cursor.fetchall()[0][0])
    sql = """
    select 
        * 
    from 
    (
        select 
            pool.`owner`,
            sum(mechine.v) as x
        from 
            pool, 
            mechine
        where 
            mechine.pid = pool.pid and 
            mechine.status_now='MiningIdle'
        group by pool.`owner`
    ) as y 
    order by x desc 
    limit 10
    """
    cursor.execute(sql)
    res_list = cursor.fetchall()
    top10_list = []
    for item in res_list:
        top10_list.append({
            "addr": item[0],
            "v" : float(item[1])
        })
    addrs = []
    for item in top10_list:
        addrs.append(item["addr"])
    names = GetAccountName(addrs)
    for i,item in enumerate(names):
        top10_list[i]["name"] = item
        top10_list[i]["percent"] =top10_list[i]["v"]/all_v
    for item in top10_list:
        sql = "insert into statistic_top10_owner(name, addr, v, percent,update_time) values('%s', '%s', %02f,%02f, %d)"%(
            item["name"],
            item["addr"],
            item["v"],
            item["percent"],
            time.time())
        cursor.execute(sql)
    db.commit()
    
def StatisticTop10Staker():
    print("start statistic top10 staker")
    cursor = db.cursor()
    time_now = time.strftime("%Y-%m-%d", time.localtime())
    sql = "delete from  statistic_top10_staker"
    cursor.execute(sql)
    sql = "select sum(locked) from staker ;"
    cursor.execute(sql)
    all_amount = float(cursor.fetchall()[0][0])
    sql = """
    select 
    *
    from (
        select 
        addr,
        sum(locked) as l
         
        from 
        staker
        group by addr 
    ) as x
    order by l desc
    limit 10
    """
    cursor.execute(sql)
    res_list = cursor.fetchall()
    top10_list = []
    for item in res_list:
        top10_list.append({
            "addr": item[0],
            "amount" : float(item[1])
        })
    addrs = []
    for item in top10_list:
        addrs.append(item["addr"])
    names = GetAccountName(addrs)
    for i,item in enumerate(names):
        top10_list[i]["name"] = item
        top10_list[i]["percent"] =top10_list[i]["amount"]/all_amount
    for item in top10_list:
        sql = "insert into statistic_top10_staker(name, addr, amount, percent,update_time) values('%s', '%s', %02f,%02f, %d)"%(
            item["name"],
            item["addr"],
            item["amount"],
            item["percent"],
            time.time())
        cursor.execute(sql)
    db.commit()
    
def UpdateLatestUpdate():
    cursor = db.cursor()
    sql = "delete  from latest_update"
    cursor.execute(sql)
    sql = "insert into latest_update(update_time) values(%d)"%(time.time())
    cursor.execute(sql)
    db.commit()
    
if __name__ == "__main__":
    while True:
        ClaimWorkers()
        ClaimStaker()
        UpdateMechinCount()
        UpdateStaking()
        StatisticTop10Owner()
        StatisticTop10Staker()
        UpdateLatestUpdate()