import os
from typing import List
import uvicorn
from BCEmbedding import RerankerModel
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

# 环境变量传入
sk_key = os.environ.get('sk-key', 'sk-aaabbbcccdddeeefffggghhhiiijjjkkk...')

# 创建一个FastAPI实例
app = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)

# 创建一个HTTPBearer实例
security = HTTPBearer()

# 初始化模型
model = RerankerModel(model_name_or_path="D:/model/bge-reranker-v2-m3")


class ReRankRequest(BaseModel):
    textList: List[str]
    query: str


class ReRankResponse(BaseModel):
    rerank_passages: List[str]
    rerank_scores: List[float]
    rerank_ids: List[int]


# 定义路由，处理rerank请求
@app.post("/v1/reRank", response_model=ReRankResponse)
async def get_embeddings(request: ReRankRequest, credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != sk_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization code",
        )
    query = request.query
    passages = request.textList
    return model.rerank(query, passages)


# 运行应用
if __name__ == "__main__":
    uvicorn.run("rerank:app", host='0.0.0.0', port=6010, workers=2)
