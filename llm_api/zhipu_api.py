# -*- coding: utf-8 -*-

import zhipuai
import time
import requests
#替换为自己的apikey
zhipuai.api_key = "6dc1fa42ad476a65c4e8ecfe94f9a127.wMiPAp0X3Q089VS5"
DATA = {
        "prompt": [
            {
                "role": "经验丰富的医生",
                "content": "根据文本内容按照以下步骤实体和三元组抽取，并严格按照步骤4要求的json格式要求输出抽取结果，不要输出多余内容；1.文本内容为{【摘要】 肺癌在中国的发病率和死亡率均位于恶性肿瘤中的第 1位。为进一步规范中国肺癌的防治措施、提高肺癌的诊疗水平、改善患者的预后、为各级临床医务人员提供专业的循证医学建议，中华医学会肿瘤学分会组织呼吸内科、肿瘤内科、胸外科、放疗科、影像科和病理科专家，以国家批准的应用指征为原则，以国内实际可应用的药品为基础，结合国际指南推荐意见和中国临床实践现状，整合近年来肺癌筛查、诊断、病理、基因检测、免疫分子标志物检测和治疗手段以及随访等诊治方面的最新循证医学证据，经过共识会议制定了中华医学会肿瘤学分会肺癌临床诊疗指南（2022 版），旨在为各级临床医师、影像、检验、康复等专业人员提供合理的推荐建议。【关键词】 肺肿瘤； 诊断； 治疗； 指南原发性支气管肺癌简称肺癌，是我国及世界各国发病率和死亡率较高的恶性肿瘤之一} 2.设定待抽取的实体类型有: 疾病、症状、科室、检查指标、检查指标结果、检查项目； 3.从上述文本中按照设定的实体类型信息抽取出对应的实体，实体抽取结果的输出json格式为:\n {\n \"entity\":\n{\"disease\":[],\n \"symptom\":[], \n \"drug \":[], \n \"department\":[], \n \"index\":[], \n \"result\":[], \n \"check\":[] \n} \n} 7.请严格按照步骤4中的要求输出，且只输出要求的JSON内容，不要输出其他多余内容。 "
            }
        ]
    }

#同步调用方式（调用后可一次性获取最终结果）
def invoke_example():
    response = zhipuai.model_api.invoke(
        model="chatglm_turbo",
        prompt=[{"role": "经验丰富的医生", "content": "根据文本内容按照以下步骤实体和三元组抽取，并严格按照步骤4要求的json格式要求输出抽取结果，不要输出多余内容；1.文本内容为{【摘要】 肺癌在中国的发病率和死亡率均位于恶性肿瘤中的第 1位。为进一步规范中国肺癌的防治措施、提高肺癌的诊疗水平、改善患者的预后、为各级临床医务人员提供专业的循证医学建议，中华医学会肿瘤学分会组织呼吸内科、肿瘤内科、胸外科、放疗科、影像科和病理科专家，以国家批准的应用指征为原则，以国内实际可应用的药品为基础，结合国际指南推荐意见和中国临床实践现状，整合近年来肺癌筛查、诊断、病理、基因检测、免疫分子标志物检测和治疗手段以及随访等诊治方面的最新循证医学证据，经过共识会议制定了中华医学会肿瘤学分会肺癌临床诊疗指南（2022 版），旨在为各级临床医师、影像、检验、康复等专业人员提供合理的推荐建议。【关键词】 肺肿瘤； 诊断； 治疗； 指南原发性支气管肺癌简称肺癌，是我国及世界各国发病率和死亡率较高的恶性肿瘤之一} 2.设定待抽取的实体类型有: 疾病、症状、科室、检查指标、检查指标结果、检查项目； 3.从上述文本中按照设定的实体类型信息抽取出对应的实体，实体抽取结果的输出json格式为:\n {\n \"entity\":\n{\"disease\":[],\n \"symptom\":[], \n \"drug \":[], \n \"department\":[], \n \"index\":[], \n \"result\":[], \n \"check\":[] \n} \n} 7.请严格按照步骤4中的要求输出，且只输出要求的JSON内容，不要输出其他多余内容。"}],
        top_p=0.7,
        temperature=0.9,
    )
    return response


#调用后会立即返回一个任务 ID ，然后用任务ID查询调用结果（根据模型和参数的不同，通常需要等待10-30秒才能得到最终结果）
def async_invoke_example():
    response_total = zhipuai.model_api.async_invoke(
        model="chatglm_turbo",
        prompt=[{"role": "经验丰富的医生", "content": "根据文本内容按照以下步骤实体和三元组抽取，并严格按照步骤4要求的json格式要求输出抽取结果，不要输出多余内容；1.文本内容为{【摘要】 肺癌在中国的发病率和死亡率均位于恶性肿瘤中的第 1位。为进一步规范中国肺癌的防治措施、提高肺癌的诊疗水平、改善患者的预后、为各级临床医务人员提供专业的循证医学建议，中华医学会肿瘤学分会组织呼吸内科、肿瘤内科、胸外科、放疗科、影像科和病理科专家，以国家批准的应用指征为原则，以国内实际可应用的药品为基础，结合国际指南推荐意见和中国临床实践现状，整合近年来肺癌筛查、诊断、病理、基因检测、免疫分子标志物检测和治疗手段以及随访等诊治方面的最新循证医学证据，经过共识会议制定了中华医学会肿瘤学分会肺癌临床诊疗指南（2022 版），旨在为各级临床医师、影像、检验、康复等专业人员提供合理的推荐建议。【关键词】 肺肿瘤； 诊断； 治疗； 指南原发性支气管肺癌简称肺癌，是我国及世界各国发病率和死亡率较高的恶性肿瘤之一} 2.设定待抽取的实体类型有: 疾病、症状、科室、检查指标、检查指标结果、检查项目； 3.从上述文本中按照设定的实体类型信息抽取出对应的实体，实体抽取结果的输出json格式为:\n {\n \"entity\":\n{\"disease\":[],\n \"symptom\":[], \n \"drug \":[], \n \"department\":[], \n \"index\":[], \n \"result\":[], \n \"check\":[] \n} \n} 7.请严格按照步骤4中的要求输出，且只输出要求的JSON内容，不要输出其他多余内容。"}],
        top_p=0.7,
        temperature=0.9,
    )

    response_data = response_total.get('data')
    response_taskId = response_data.get("task_id")

    response = zhipuai.model_api.query_async_invoke_result(response_taskId)
    # print(response)
    return response


#sse调用方式
'''
  说明：
  add: 事件流开启
  error: 平台服务或者模型异常，响应的异常事件
  interrupted: 中断事件，例如：触发敏感词
  finish: 数据接收完毕，关闭事件流
'''


#调用后可以流式的实时获取到结果直到结束
def sse_invoke_example():
    response = zhipuai.model_api.sse_invoke(
        model="chatglm_turbo",
        prompt=[{"role": "经验丰富的医生", "content": "根据文本内容按照以下步骤实体和三元组抽取，并严格按照步骤4要求的json格式要求输出抽取结果，不要输出多余内容；1.文本内容为{【摘要】 肺癌在中国的发病率和死亡率均位于恶性肿瘤中的第 1位。为进一步规范中国肺癌的防治措施、提高肺癌的诊疗水平、改善患者的预后、为各级临床医务人员提供专业的循证医学建议，中华医学会肿瘤学分会组织呼吸内科、肿瘤内科、胸外科、放疗科、影像科和病理科专家，以国家批准的应用指征为原则，以国内实际可应用的药品为基础，结合国际指南推荐意见和中国临床实践现状，整合近年来肺癌筛查、诊断、病理、基因检测、免疫分子标志物检测和治疗手段以及随访等诊治方面的最新循证医学证据，经过共识会议制定了中华医学会肿瘤学分会肺癌临床诊疗指南（2022 版），旨在为各级临床医师、影像、检验、康复等专业人员提供合理的推荐建议。【关键词】 肺肿瘤； 诊断； 治疗； 指南原发性支气管肺癌简称肺癌，是我国及世界各国发病率和死亡率较高的恶性肿瘤之一} 2.设定待抽取的实体类型有: 疾病、症状、科室、检查指标、检查指标结果、检查项目； 3.从上述文本中按照设定的实体类型信息抽取出对应的实体，实体抽取结果的输出json格式为:\n {\n \"entity\":\n{\"disease\":[],\n \"symptom\":[], \n \"drug \":[], \n \"department\":[], \n \"index\":[], \n \"result\":[], \n \"check\":[] \n} \n} 7.请严格按照步骤4中的要求输出，且只输出要求的JSON内容，不要输出其他多余内容。"}],
        top_p=0.7,
        temperature=0.9,
    )


    current_total_response_data = ""

    # response不为空
    if response.events() is not None:
        for event in response.events():  # event = add …… add,finish
            if event.event == "add":
                current_total_response_data += event.data
                # print(event.data)
            elif event.event == "error" or event.event == "interrupted":
                print(event.data)
            elif event.event == "finish":  # type(event.data)=<class 'str'>
                current_total_response_data += event.data
            else:
                print(event.data)


    # 为空就标记一下，进入下次循环
    else:
        current_total_response_data = None
        print("回复为空, 继续执行")
    return current_total_response_data


def query_async_invoke_result_example():
    response = zhipuai.model_api.query_async_invoke_result("your task_id")
    print(response)

if __name__ == '__main__':

    #同步调用方式
    invoke_start_time = time.time()
    invoke_response = invoke_example()
    invoke_end_time = time.time()
    invoke_elapsed_time = invoke_end_time - invoke_start_time
    print("invoke同步调用 单chunk测试所用时间")
    print(invoke_elapsed_time)    #5.952698707580566
    print(invoke_response)

    # #异步调用方式
    # async_start_time = time.time()
    # async_response = async_invoke_example()
    # async_end_time = time.time()
    # async_elapsed_time = async_end_time - async_start_time
    # print("async异步调用 单chunk测试所用时间")   #1.0345392227172852
    # print(async_elapsed_time)
    # print(async_response)
    #
    # #sse调用方式
    # sse_start_time = time.time()
    # sse_response = sse_invoke_example()
    # sse_end_time = time.time()
    # sse_elapsed_time = sse_end_time - sse_start_time
    # print("sse调用 单chunk测试所用时间")
    # print(sse_elapsed_time)    #5.917327642440796
    # print(sse_response)