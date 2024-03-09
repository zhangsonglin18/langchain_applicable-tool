import os
from app.api.movies_search import mv_v1 as blueprint
from fastapi import FastAPI, File, UploadFile
from utils.encode import SentenceModel
from data_conn.milvus2.milvus_helpers import MilvusHelper
from data_conn.mysql8.mysql_helpers import MySQLHelper
from config.configs import UPLOAD_PATH
from utils.logs import LOGGER
from program.mvlivus_recom.milvus_pro import Milvus_pro


MODEL = SentenceModel()
MILVUS_CLI = MilvusHelper()
MYSQL_CLI = MySQLHelper()
Milvus_pc = Milvus_pro()

# Mkdir '/tmp/qa-data'
if not os.path.exists(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)


@blueprint.post('/qa/load_data')
async def do_load_api(file: UploadFile = File(...), table_name: str = None):
    try:
        text = await file.read()
        fname_path = os.path.join(UPLOAD_PATH, file.filename)
        with open(fname_path, 'wb') as f:
            f.write(text)
        total_num = Milvus_pc.do_load(table_name, fname_path, MODEL, MILVUS_CLI, MYSQL_CLI)
        LOGGER.info(f"Successfully loaded data, total count: {total_num}")
        return {'status': True, 'msg': f"Successfully loaded data: {total_num}"}, 200
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}, 400


@blueprint.get('/qa/search')
async def do_get_question_api(question: str, table_name: str = None):
    try:
        questions, _= Milvus_pc.do_search(table_name, question, MODEL, MILVUS_CLI, MYSQL_CLI)
        LOGGER.info("Successfully searched similar images!")
        return {'status': True, 'msg': questions}, 200
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}, 400


@blueprint.get('/qa/answer')
async def do_get_answer_api(question: str, table_name: str = None):
    try:
        results = Milvus_pc.do_get_answer(table_name, question, MYSQL_CLI)
        return {'status': True, 'msg': results}
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}


@blueprint.post('/qa/count')
async def count_images(table_name: str = None):
    try:
        num = Milvus_pc.do_count(table_name, MILVUS_CLI)
        LOGGER.info("Successfully count the number of questions!")
        return num
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}, 400


@blueprint.post('/qa/drop')
async def drop_tables(table_name: str = None):
    try:
        status = Milvus_pc.do_drop(table_name, MILVUS_CLI, MYSQL_CLI)
        LOGGER.info("Successfully drop tables in Milvus and MySQL!")
        return {'status': True, 'msg': status}
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}, 400