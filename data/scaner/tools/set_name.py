import pymysql
db_online = pymysql.connect("pha_mysql","root","123456","phala" )
cursor = db_online.cursor()
file = open("./mechine_name", "r")
lines = file.readlines()
print(len(lines))
mechine_list = []

for line in lines:
    line = line.replace("\n", "")
    item = line.split("\t")
    if len(item) == 2 and len(item[1]) == 64:
        sql = "update mechine set name = '%s' where pubkey = '0x%s'"%(item[0], item[1]);
        cursor.execute(sql)
db_online.commit()
        