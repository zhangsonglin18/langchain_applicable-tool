import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from operator import itemgetter
from FlagEmbedding import FlagReranker


app = FastAPI()

reranker = FlagReranker('D:/model/bge-reranker-v2-m3', use_fp16=True)


class QuerySuite(BaseModel):
    query: str
    passages: list[str]
    top_k: int = 1


@ app.post('/bge_base_rerank')
def rerank(query_suite: QuerySuite):
    scores = reranker.compute_score([[query_suite.query, passage] for passage in query_suite.passages])
    if isinstance(scores, list):
        similarity_dict = {passage: scores[i] for i, passage in enumerate(query_suite.passages)}
    else:
        similarity_dict = {passage: scores for i, passage in enumerate(query_suite.passages)}
    sorted_similarity_dict = sorted(similarity_dict.items(), key=itemgetter(1), reverse=True)
    result = {}
    for j in range(query_suite.top_k):
        result[sorted_similarity_dict[j][0]] = sorted_similarity_dict[j][1]
    return result


if __name__ == '__main__':
    query = "电子科技大学的官网？"
    docs = [
        "院校&专业高考备考高一/高二家长助考新东方网主站中学高考高考资讯焦点新闻电子科技大学：2022年全国招生总计划5030人 招生专业上有“三变化”新东方编辑整理 |2023-03-13 15:04  分享至  复制链接1.请使用微信扫码2.打开网页后点击屏幕右上角分享按钮",
        "拉斯哥大学交流学习的机会，也可以申请3+2、4+1等海外联合培养模式。师资主要由电子科技大学与格拉斯哥大学的优秀老师进行授课。毕业时所颁发的毕业证与学位证与“电子科技大学”招生名称的证书完全一致，同时还能获得格拉斯哥大学的学位证书。由于是首年进行招生，这个项目可能会成为今年填报志愿的价值洼地。",
        "其次是深造情况，近十年学校深造率不断提升，最近两届毕业生深造率继续保持高位超过70%，位居全国所有高校的第4位。国内深造学生到双一流高校及研究院所深造的比例超过了99%，在出国（境）深造的学生中，去往世界前100位的大学就读占比超过70%。所以同样的，我们在深造方面，也是不仅深造率高，同样深造的质量也是非常高的。九、学校咨询方式或联系方式。1.信息平台微信公众号：电子科大本科招生（uestc_zs）官网：http://www.zs.uestc.edu.cn/",
        "二、2022年学校招生计划如何安排？有无增减？今年电子科技大学的招生总规模与往年相比，维持相对的稳定。2022年，我们在全国招生总计划是5030人，其中“电子科技大学”将面向全国招生3300余人，“电子科技大学（沙河校区）”将面向部分省份招生1700余人。电子科技大学将继续采用“电子科技大学”、“电子科技大学（沙河校区）”两个名称进行招生，考生在填报志愿时应分别填报，录取时分别录取，对应着不同的录取分数线。"]

    # uvicorn.run(app, host='0.0.0.0', port=50072)