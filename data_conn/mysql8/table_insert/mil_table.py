from data_conn.mysql8.mysql_conn import *
import json
mysql = MySql()

if __name__ == '__main__':
    # create_table_query = """
    # CREATE TABLE IF NOT EXISTS miti (
    #     id INT AUTO_INCREMENT PRIMARY KEY,
    #     oid VARCHAR(255) NOT NULL,
    #     `name1` VARCHAR(255) NOT NULL,
    #     country VARCHAR(2048) NOT NULL,
    #     `images` VARCHAR(1024) NOT NULL,
    #     `introduction` VARCHAR(4086) NOT NULL,
    #     `first_flight` VARCHAR(255) NOT NULL,
    #     `service_entry` VARCHAR(255) NOT NULL,
    #     `developer` VARCHAR(255) NOT NULL,
    #     `producer` VARCHAR(255) NOT NULL,
    #     `length` VARCHAR(255) NOT NULL,
    #     `wingspan` VARCHAR(255) NOT NULL,
    #     `height` VARCHAR(255) NOT NULL,
    #     `empty_weight` VARCHAR(255) NOT NULL,
    #     `engine_type` VARCHAR(255) NOT NULL,
    #     `maximum_weight` VARCHAR(255) NOT NULL,
    #     `maximum_speed` VARCHAR(255) NOT NULL,
    #     `maximum_distence` VARCHAR(255) NOT NULL,
    #     `category` VARCHAR(255) NOT NULL,
    #     `type` VARCHAR(255) NOT NULL)
    #     """
    # mysql.create_table(create_table_query)
    # query = ''
    path = "D:\\model\\data_set\\military.json"
    tmp = []
    total = []
    for line in open(path,'r', encoding='utf-8'):
        tmp.append(json.loads(line))
    # data = pd.read_excel(path, header=0, engine='openpyxl')
    # {"_id": {"$oid": "5cc9308f831b973d657f0f4f"}, "名称": "FC-1“枭龙”/JF-17“雷电”多用途攻击机", "产国": "中国",
    #  "图片": "http://images.huanqiu.com/sarons/2013/07/b55691d07181302014e736c49034c16a.jpg",
    #  "简介": "\nFC-1枭龙战斗机是中国研制的一种全天候、单发、单座、轻型超音速战斗机，具有完全自主知识产权的多用途轻型战斗机，由中国航空工业第一集团公司与巴基斯坦空军共同出资，由成都飞机设计研究所、成都飞机工业集团公司与巴基斯坦航空综合企业（Pakistan Aeronautical Complex）合作研制的多用途单座单发轻型战机。\n\nFC-1枭龙战斗机2002年5月31日完成设计，2003年8月25日首次试飞。2007年开始交付巴基斯坦空军。2013年5月22日，李克强总理从印度飞往巴基斯坦开始访问，进入巴境后，巴基斯坦6架枭龙战机为李总理专机全程护航。\n",
    #  "首飞时间": "2003年8月25日", "服役时间": "2007年3月12日", "研发单位": "成都飞机公司",
    #  "生产单位": "成都飞机公司，巴基斯坦航空综合企业", "气动布局": "后掠翼", "发动机数量": "单发", "飞行速度": "超音速",
    #  "关注度": "(4分)", "乘员": "1人", "机长": "14.93米", "翼展": "9.46米", "机高": "4.78米", "空重": "6586千克",
    #  "发动机": "俄制RD-93发动机", "最大起飞重量": "12383千克", "最大飞行速度": "1960千米每小时", "最大航程": "3482千米",
    #  "大类": "飞行器", "类型": "战斗机"}
    for item in tmp:
        print(item)
        oid = item["_id"]["$oid"]
        name1 = item["名称"]
        country = item["产国"]
        images = item["图片"]
        introduction = item["简介"]
        first_flight = item["首飞时间"]
        try:
            service_entry = item["服役时间"]
        except:
            service_entry =[]
        try:
            developer = item["研发单位"]
        except:
            developer = []
        try:
            producer = item["生产单位"]
        except:
            producer =[]
        length= item["机长"]
        wingspan= item["翼展"]
        height= item["机高"]
        empty_weight= item["空重"]
        engine_type= item["发动机"]
        maximum_weight= item["最大起飞重量"]
        maximum_speed= item["最大飞行速度"]
        maximum_distence= item["最大航程"]
        category= item["大类"]
        type= item["类型"]
        print(height)
        # query = '''('{}', '{}', '{}','{}','{}','{}','{}')'''.format(published, title, content, country, abstract_text,
        #                                                             external_images, entities)
        # sql = '''INSERT INTO news1 (published, `title`, `content`, country, `abstract_text`,`external_images`, `entities`) VALUES''' + query  # 完整的sql语句
        # mysql.insert_data(sql, "")

