import os
from langchain.evaluation import load_evaluator, EvaluatorType, Criteria
from langchain.chat_models import ChatOpenAI
from pprint import pprint
from llm_api.openai_api import openai
evaluation_llm = openai().chat_model()
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# evaluation_llm = ChatOpenAI(model="gpt-4", temperature=0)

# evaluator = load_evaluator(EvaluatorType.CRITERIA,
#                            criteria=Criteria.CONCISENESS,
#                            llm=evaluation_llm)
#
# eval_result = evaluator.evaluate_strings(
#     prediction="What's 2+2? That's an elementary question. The answer you're looking for is that two and two is four.",
#     input="What's 2+2?",
# )
# pprint(eval_result)

evaluator = load_evaluator(EvaluatorType.CONTEXT_QA,
                           criteria=Criteria.CORRECTNESS,
                           llm=evaluation_llm,
                           requires_reference=True)

question = "2022年上海的常住人口是多少?"
context = "上海市，简称沪。 是中华人民共和国直辖市、中国共产党诞生地、国家中心城市、超大城市 、上海大都市圈核心城市、中国历史文化名城、" \
          "世界一线城市。 上海基本建成国际经济、金融、贸易、航运中心，形成具有全球影响力的科技创新中心基本框架。" \
          "上海市总面积6340.5平方千米，辖16个区。 2022年，上海市常住人口为2475.89万人。"
pred = "2022年，上海市的常住人口为2475万人。"
# evaluate
eval_result = evaluator.evaluate_strings(
  input=question,
  prediction=pred,
  reference=context
)
print(eval_result)