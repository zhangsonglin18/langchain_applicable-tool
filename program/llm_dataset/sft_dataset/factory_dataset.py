import json
#
result = []
with open("D:/model/data_set/sft_dataset/dev_data_clean_deep.json", "r",encoding="utf-8") as file:
    data = json.loads(file.read())
    prompt = "给出如下参考新闻内容，抽取该新闻中的实体信息包括实体类型type和实体结果entity，并生成的格式如[{'type': 'ORG', 'entity': '俄罗斯国防部'}, {'type': 'TIM', 'entity': '17日'}, {'type': 'NUM', 'entity': '1架'}]所示，其中参考新闻如下所示："
    for item in data:
        res = {}
        res["instruction"] = prompt
        res["input"] = item["text"]
        rest = []
        for enti in item["entities"]:
            rest.append({"type": enti["type"], "entity": enti["entity"]})
        res["output"] = str(rest)
        result.append(res)

prompt_e = "给出如下参考新闻内容，抽取该新闻中的事件信息，并生成的事件抽取结果格式如[{'label': '时间', 'entity': '12月19日'}, {'label': '主动方', 'entity': '肥西县上派镇组织镇人大代表'}, {'label': '领导视察触发词', 'entity': '视察'}, {'label': '视察内容', 'entity': '重点片区征迁工作'}]所示，其中参考新闻如下所示："
with open("D:/model/data_set/sft_dataset/19all.txt", "r",encoding="utf-8") as file:
    for line in file:
        res = {}
        item = json.loads(line)
        text = item["text"]
        content = item["entities"]
        resu = []
        for entity in content:
            entity["entity"] = text[entity["start_offset"]:entity["end_offset"]]
            resu.append({'label':entity["label"],'entity':entity["entity"]})
        res["instruction"] = prompt_e
        res["input"] = item["text"]
        res["output"] = str(resu)
        result.append(res)
print(result)
filename = "data.jsonl"
# 打开文件进行写入
# with open(filename, 'w',encoding="utf-8") as f:
#     for data in result:
#         json.dump(data, f,ensure_ascii=False)  # 使用json.dump()直接将字典转换为JSON写入文件
#         f.write('\n')  # 在每个JSON对象后添加换行符

with open('data.json', 'w',encoding="utf-8") as json_file:
    json.dump(result, json_file,ensure_ascii=False,indent=4)
