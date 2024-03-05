import pymysql
# 建立与数据库的连接
conn = pymysql.connect(host='101.200.135.154', port=33306, user='root', password='123456',
                       database='information_schema')
cursor = conn.cursor()

# 执行查询语句
sql = "SELECT * FROM FILES"
cursor.execute(sql)
result = cursor.fetchall()
for row in result:
    print(row)
# 关闭连接
cursor.close()
conn.close()