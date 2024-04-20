import json
#
result = []
with open("D:/model/data_set/sft_dataset/dev_data_clean_deep.json", "r",encoding="utf-8") as file:
    data = json.loads(file.read())
    prompt = "给出如下参考新闻内容，抽取该新闻中的实体信息包括实体类型type和实体结果entity，并生成的格式如[{'type': 'ORG', 'entity': '俄罗斯国防部'}, {'type': 'TIM', 'entity': '17日'}, {'type': 'NUM', 'entity': '1架'}]所示，其中参考新闻如下所示："
    for item in data:
        res = {}
        res["kind"] = "NER"
        res["input"] = prompt+item["text"]
        rest = []
        for enti in item["entities"]:
            rest.append({"type": enti["type"], "entity": enti["entity"]})
        res["target"] = str(rest)
        result.append(res)

prompt_e = "给出如下参考新闻内容，抽取该新闻中的事件信息，其中label包括时间、主动方、触发词、触发词包含内容等关键信息，并生成的事件抽取结果格式如[{'label': '时间', 'entity': '12月19日'}, {'label': '主动方', 'entity': '肥西县上派镇组织镇人大代表'}, {'label': '领导视察触发词', 'entity': '视察'}, {'label': '视察内容', 'entity': '重点片区征迁工作'}]所示，其中参考新闻如下所示："
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
        res["kind"] = "IEE"
        res["input"] = prompt_e+item["text"]
        res["target"] = str(resu)
        result.append(res)
print(result)
# with open('data1.json', 'w',encoding="utf-8") as json_file:
#     json.dump(result, json_file,ensure_ascii=False,indent=4)
# json_data = json.dumps(result,ensure_ascii=False, indent=4)
# 将 json 数据写入文件
with open('data1.json','w',encoding="utf-8") as json_file:
    for data in result:
        # json.dump(data, json_file,ensure_ascii=False, indent=4)
        json_file.write(json.dumps(data,ensure_ascii=False))
        json_file.write('\n')
# import json
# text = str({'kind': 'NER', 'input': "给出如下参考新闻内容，抽取该新闻中的实体信息包括实体类型type和实体结果entity，并生成的格式如[{'type': 'ORG', 'entity': '俄罗斯国防部'}, {'type': 'TIM', 'entity': '17日'}, {'type': 'NUM', 'entity': '1架'}]所示，其中参考新闻如下所示：雷达反射面仅为B-52H的百分之一，****B-2A“幽灵”隐身战略轰炸机，作战半径6000千米，最大飞行时速1164千米，载弹量22680千克，正常探测距离下，雷达反射面积仅与一只小鸟相当，这些战略轰炸机从美国本土或海外基地起飞，经空中加油后，可以飞抵全球任何地方，且杀伤力巨大，打击精度也很高，美军还高度重视发展无人机系统，使无人机数量不断攀升、性能持续提高，目前有1万余架，其中不少无人机已在阿富汗等战场发挥重要作用，这些无人机既能侦察监视，也能执行对地打击任务，", 'target': "[{'type': 'WEA', 'entity': 'B-52H'}, {'type': 'WEA', 'entity': 'B-2A“幽灵”隐身战略轰炸机'}, {'type': 'NUM', 'entity': '6000千米'}, {'type': 'NUM', 'entity': '1164千米'}, {'type': 'NUM', 'entity': '22680千克'}, {'type': 'NUM', 'entity': '一只'}, {'type': 'LOC', 'entity': '美国'}, {'type': 'ORG', 'entity': '美军'}, {'type': 'NUM', 'entity': '1万余架'}, {'type': 'LOC', 'entity': '阿富汗'}]"})
# data = json.loads(text)
# print(data)