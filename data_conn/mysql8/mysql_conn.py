import pymysql
from config.configs import Congif
import pandas as pd
# 建立与数据库的连接

class MySql():
    def __init__(self):
        self.conn = pymysql.connect(host=Congif.sql_host, port=Congif.sql_port, user=Congif.sql_user, password=Congif.sql_password,
                           database=Congif.sql_database)
        self.cursor = self.conn.cursor()

    def sql_fetchall(self,sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def sql_fetchone(self,sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    # 执行查询语句
    def sql_search(self,sql):
        res = []
        # sql = "SELECT * FROM FILES"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for row in result:
            res.append(row)
            print(row)
        return res

    def create_table(self,create_table_query):
        # create_table_query = """
        # CREATE TABLE IF NOT EXISTS your_table_name (
        #     id INT AUTO_INCREMENT PRIMARY KEY,
        #     column1 VARCHAR(255) NOT NULL,
        #     column2 INT,
        #     column3 DATE
        # )
        # """
        try:
            # 执行SQL语句创建表
            self.cursor.execute(create_table_query)
            # 提交到数据库执行
            self.conn.commit()
            print("Table created successfully")
        except pymysql.Error as err:
            # 如果有错误，打印错误消息
            print(f"Error: {err}")

    def close_sql(self):
        if self.cursor and self.cursor.is_connected():
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()

    def insert_data(self,query,data):
        # query = "INSERT INTO your_table_name (column1, column2, column3) VALUES (%s, %s, %s)"
        try:
            # for item in data:
            # query = query.format(data[0],data[1],data[2],data[3])
            self.cursor.execute(query)
            self.conn.commit()
        except pymysql.Error as err:
            # 如果有错误，打印错误消息
            print(f"Error: {err}")

    def update_data(self,query,data):
        # query = "UPDATE your_table_name SET column1 = %s WHERE id = %s"
        try:
            for item in data:
                self.cursor.execute(query, item)
                self.conn.commit()
        except pymysql.Error as err:
            # 如果有错误，打印错误消息
            print(f"Error: {err}")

    def delete_data(self,query,data):
        # query = "DELETE FROM your_table_name WHERE id = %s"
        try:
            # for item in data:
            query = query.format(data[0],data[1],data[2],data[3])
            self.cursor.execute(query)
            self.conn.commit()
        except pymysql.Error as err:
            # 如果有错误，打印错误消息
            print(f"Error: {err}")

    def __call__(self, *args, **kwargs):
        try:
            print(self.conn)
        except:
            print("Error")

'''导入部分病例数据样例'''
# mysql = MySql()
# create_table_query = """
# CREATE TABLE IF NOT EXISTS sick_answer (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     department VARCHAR(255) NOT NULL,
#     title VARCHAR(255) NOT NULL,
#     `ask` VARCHAR(1250) NOT NULL,
#     `answer` VARCHAR(1250) NOT NULL,
#     types VARCHAR(255) NOT NULL
#
# )
# """
# mysql.create_table(create_table_query)
# path = "D:\\model\\data_set\\Chinese-medical-dialogue-data\\Data_数据\\IM_内科\\内科5000-33000.csv"
# data = pd.read_csv(path, encoding='ANSI')
# ##多文件导入
# query = ''
# for index, row in data.iterrows():
#     ask = row["ask"]
#     answer = row["answer"]
#     department = row["department"]
#     title = row["title"]
#     types = "Andriatria_男科"
#     # query += ('''INSERT INTO man_sick (department, title, ask,answer,types) VALUES ('{}', '{}', '{}','{}','{}')'''.
#     #           format(department, title, ask,answer,types))
#     query += '''('{}', '{}', '{}','{}','{}'),'''.format(department, title, ask, answer, types)
#     if index%1000 == 0:
#         sql = query[:-1]  # 去除最后一个逗号获得所有行记录的拼接
#         sql = '''INSERT INTO sick_answer (department, title, `ask`, `answer`,types) VALUES''' + sql  # 完整的sql语句
#         mysql.insert_data(sql, "")
#         query = ''
#         print("________________")


if __name__ == '__main__':
    mysql = MySql()
    query = "SELECT * FROM `q_intelligence`.`sick_answer` WHERE `department` LIKE '%内分泌%' AND `ask` LIKE '%糖尿病%' LIMIT 0,10"
    data = mysql.sql_search(query)
    print(data)






