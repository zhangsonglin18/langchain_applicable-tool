from data_conn.mysql8.mysql_conn import *
mysql = MySql()

##creat_news_table
# mysql.delete_all_data("news1")
# create_table_query = """
# CREATE TABLE IF NOT EXISTS news1 (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     published DATE NOT NULL,
#     `title` VARCHAR(1025) NOT NULL,
#     `content` VARCHAR(4086) NOT NULL,
#     country VARCHAR(2048) NOT NULL,
#     `abstract_text` VARCHAR(4086) NOT NULL,
#     `external_images` VARCHAR(1024) NOT NULL,
#     `entities` VARCHAR(4086) NOT NULL)
#     """
# mysql.create_table(create_table_query)
# # query = ''
# path = "D:\\model\\data_set\\tadmin_kyqb.xlsx"
# data = pd.read_excel(path, header=0, engine='openpyxl')
# for index, row in data.iterrows():
#     published = row["published"]
#     title = row["title_translate"]
#     content = row["text_translate"]
#     country = row["country"]
#     abstract_text = row["abstract_text"]
#     external_images = row["external_images"]
#     try:
#         entities = row["entities"].encode('ANSI').decode('unicode_escape')
#         print(entities)
#     except:
#         entities = []
#     # query += ('''INSERT INTO man_sick (department, title, ask,answer,types) VALUES ('{}', '{}', '{}','{}','{}')'''.
#     #           format(department, title, ask,answer,types))
#     query = '''('{}', '{}', '{}','{}','{}','{}','{}')'''.format(published, title, content, country, abstract_text,
#                                                                 external_images, entities)
#     sql = '''INSERT INTO news1 (published, `title`, `content`, country, `abstract_text`,`external_images`, `entities`) VALUES''' + query  # 完整的sql语句
#     mysql.insert_data(sql, "")
# #     if index%1 == 0:
# #         sql = query[:-1]  # 去除最后一个逗号获得所有行记录的拼接
# #         sql = '''INSERT INTO news1 (published, `title`, `content`, country, `abstract_text`,`external_images`, `entities`) VALUES''' + sql  # 完整的sql语句
# #         mysql.insert_data(sql, "")
# #         query = ''
# #         print("________________")
if __name__ == '__main__':
    mysql = MySql()
    query = "SELECT id,external_images FROM `q_intelligence`.`news1`"
    data = mysql.sql_search(query)
    print(data)


