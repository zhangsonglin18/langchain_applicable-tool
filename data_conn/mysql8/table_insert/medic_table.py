from data_conn.mysql8.mysql_conn import *
mysql = MySql()
create_table_query = """
CREATE TABLE IF NOT EXISTS sick_answer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    department VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    `ask` VARCHAR(1250) NOT NULL,
    `answer` VARCHAR(1250) NOT NULL,
    types VARCHAR(255) NOT NULL

)
"""
mysql.create_table(create_table_query)
path = "D:\\model\\data_set\\Chinese-medical-dialogue-data\\Data_数据\\IM_内科\\内科5000-33000.csv"
data = pd.read_csv(path, encoding='ANSI')
##多文件导入
query = ''
for index, row in data.iterrows():
    ask = row["ask"]
    answer = row["answer"]
    department = row["department"]
    title = row["title"]
    types = "Andriatria_男科"
    # query += ('''INSERT INTO man_sick (department, title, ask,answer,types) VALUES ('{}', '{}', '{}','{}','{}')'''.
    #           format(department, title, ask,answer,types))
    query += '''('{}', '{}', '{}','{}','{}'),'''.format(department, title, ask, answer, types)
    if index%1000 == 0:
        sql = query[:-1]  # 去除最后一个逗号获得所有行记录的拼接
        sql = '''INSERT INTO sick_answer (department, title, `ask`, `answer`,types) VALUES''' + sql  # 完整的sql语句
        mysql.insert_data(sql, "")
        query = ''
        print("________________")