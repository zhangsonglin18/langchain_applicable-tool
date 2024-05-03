import json
import re
#
result = []
# with open("D:/model/data_set/sft_dataset/dev_data_clean_deep.json", "r",encoding="utf-8") as file:
#     data = json.loads(file.read())
#     prompt = "给出如下参考新闻内容，抽取该新闻中的实体信息包括实体类型type和实体结果entity，并生成的格式如[{'type': 'ORG', 'entity': '俄罗斯国防部'}, {'type': 'TIM', 'entity': '17日'}, {'type': 'NUM', 'entity': '1架'}]所示，其中参考新闻如下所示："
#     for item in data:
#         res = {}
#         res["instruction"] = prompt
#         res["input"] = item["text"]
#         rest = []
#         for enti in item["entities"]:
#             rest.append({"type": enti["type"], "entity": enti["entity"]})
#         res["output"] = str(rest)
#         result.append(res)
#
# prompt_e = "给出如下参考新闻内容，抽取该新闻中的事件信息，并生成的事件抽取结果格式如[{'label': '时间', 'entity': '12月19日'}, {'label': '主动方', 'entity': '肥西县上派镇组织镇人大代表'}, {'label': '领导视察触发词', 'entity': '视察'}, {'label': '视察内容', 'entity': '重点片区征迁工作'}]所示，其中参考新闻如下所示："
# with open("D:/model/data_set/sft_dataset/19all.txt", "r",encoding="utf-8") as file:
#     for line in file:
#         res = {}
#         item = json.loads(line)
#         text = item["text"]
#         content = item["entities"]
#         resu = []
#         for entity in content:
#             entity["entity"] = text[entity["start_offset"]:entity["end_offset"]]
#             resu.append({'label':entity["label"],'entity':entity["entity"]})
#         res["instruction"] = prompt_e
#         res["input"] = item["text"]
#         res["output"] = str(resu)
#         result.append(res)
# print(result)
# prompt_ie = "给出如下参考新闻内容，抽取该新闻中的关系信息，其中生成结果必须包含[head、head_type、relation、tail、tail_type]，生成的关系抽取结果格式如 [{'head': '2018年冬季残奥会闭幕式', 'head_type': '事件', 'relation': '发生地点', 'tail': '平昌奥林匹克体育场', 'tail_type': '地理地区'}, {'head': '2018年冬季残奥会闭幕式', 'head_type': '事件', 'relation': '发生时间', 'tail': '2018年3月18日', 'tail_type': '时间'}]所示，其中参考新闻如下所示："
# with open("D:/model/data_set/extract/train_zh.json", "r",encoding="utf-8") as file:
#     for item in file:
#         data = json.loads(item)
#         res = {}
#         res["instruction"] = prompt_ie
#         res["input"] = data["text"]
#         res["output"] = str(data["relation"])
#         print(res["output"])
#         result.append(res)

with open("D:/model/data_set/extract/train.json", "r",encoding="utf-8") as file:
    for item in file:
        res = {}
        item = json.loads(item)
        res["instruction"] = json.loads(item["instruction"])["instruction"]
        schema = json.loads(item["instruction"])["schema"]
        res["input"] = json.loads(item["instruction"])["input"]
        res["output"] = item["output"]
        pattern = r'[^\u4e00-\u9fff]'
        pat = re.sub(pattern, '', res["input"][0])
        if pat:
            res["instruction"] = str(res["instruction"]) + "其中shema的格式如下所示：" + str(schema)
            print(res["instruction"])
            print(res["output"])
            result.append(res)

# with open('ie.json', 'w',encoding="utf-8") as json_file:
#     json.dump(result, json_file,ensure_ascii=False,indent=4)










