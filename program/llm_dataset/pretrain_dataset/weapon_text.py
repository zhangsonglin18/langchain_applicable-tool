import json
result = ""
with open("D:/model/data_set/military.json", "r",encoding="utf-8") as file:
    for item in file:
        items = json.loads(item)
        del items['_id']
        name = items['名称']
        rest = f"介绍一下{name}的详细情况：".format(name) + str(items) +"。"
        result += rest
with open("weapons.txt", "w", encoding="utf-8") as txt_file:
    txt_file.write(result)

