
from py2neo import *
import pandas as pd
graph = Graph("http://101.200.135.154:7474",auth=("neo4j","mmkg12#$"))
def yogadata():
    count  = 0
    frame = pd.read_csv(r"yoga.csv", encoding='gbk')
    for i in frame.index:
        '''获取数据'''
        yoga_name = frame["招式"].values[i]
        yoga_ms = frame["描述"].values[i]
        yoga_yc = frame["益处"].values[i]
        yoga_zysx = frame["注意事项"].values[i]
        yoga_cjwt = frame["常见问题"].values[i]

        yoga_name = str(yoga_name)
        yoga_ms = str(yoga_ms)
        yoga_yc = str(yoga_yc)
        yoga_zysx = str(yoga_zysx)
        yoga_cjwt = str(yoga_cjwt)

        yoga_node = Node('招式', name=yoga_name)
        graph.merge(yoga_node)  ## merge方法是将重复数据去除掉，只留第一个
        ms_node = Node('描述', name=yoga_ms)
        yc_node = Node('益处', name=yoga_yc)
        zysx_node = Node('注意事项', name=yoga_zysx)
        cjwt_node = Node('常见问题', name=yoga_cjwt)

        # 瑜伽类
        yoga_2 = Relationship(yoga_node, '描述', ms_node)
        yoga_3 = Relationship(yoga_node, '益处', yc_node)
        yoga_4 = Relationship(yoga_node, '注意事项', zysx_node)
        yoga_5 = Relationship(yoga_node, '常见问题', cjwt_node)

        try:
            graph.create(yoga_2)
        except:
            continue
        try:
            graph.create(yoga_3)
        except:
            continue
        try:
            graph.create(yoga_4)
        except:
            continue
        try:
            graph.create(yoga_5)
        except:
            continue
        count += 1
        print(count)
yogadata()

