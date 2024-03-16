from configparser import ConfigParser
import os
class BaseConfig:
    open_ai = "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"
    open_ai1 = "sk-ln0lOOW4xaCLK0nT92367a1852D744E2867d256933B8Bc35"

class BaseParams(object):
    """
    各类型参数的父类
    """

    def __init__(self, conf_fp: str = 'D:\llm_mmkg\config\config.ini'):
        self.config = ConfigParser()
        self.config.read(conf_fp, encoding='utf8')


class ModelParams(BaseParams):
    """
    数据拉取参数类
    """

    def __init__(self, conf_fp: str = 'D:\llm_mmkg\config\config.ini'):
        super(ModelParams, self).__init__(conf_fp)
        section_name = 'model_configs'
        self.embedding_model = self.config.get(section_name, 'embedding_model')
        self.llm_model = self.config.get(section_name, 'llm_model')

class ESParams(BaseParams):
    """
    数据拉取参数类
    """

    def __init__(self, conf_fp: str = 'D:\llm_mmkg\config\config.ini'):
        super(ESParams, self).__init__(conf_fp)
        section_name = 'es_configs'
        self.username = self.config.get(section_name, 'username')
        self.passwd = self.config.get(section_name, 'passwd')
        self.url = self.config.get(section_name, 'url')
        self.port = self.config.get(section_name, 'port')
        self.index_name = self.config.get(section_name, 'index_name')


class Congif():
    sql_host='101.200.135.154'
    sql_port= 33306
    sql_user='root'
    sql_password='123456'
    sql_database='q_intelligence'

############### Milvus Configuration ###############
MILVUS_HOST = os.getenv("MILVUS_HOST", "101.200.135.154")
MILVUS_PORT = int(os.getenv("MILVUS_PORT", "19530"))
VECTOR_DIMENSION = int(os.getenv("VECTOR_DIMENSION", "768"))
INDEX_FILE_SIZE = int(os.getenv("INDEX_FILE_SIZE", "1024"))
METRIC_TYPE = os.getenv("METRIC_TYPE", "IP")
DEFAULT_TABLE = os.getenv("DEFAULT_TABLE", "qa_search")
TOP_K = int(os.getenv("TOP_K", "10"))

############### MySQL Configuration ###############
MYSQL_HOST = os.getenv("MYSQL_HOST", "101.200.135.154")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "33306"))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PWD = os.getenv("MYSQL_PWD", "123456")
MYSQL_DB = os.getenv("MYSQL_DB", "q_intelligence")

############### Data Path ###############
UPLOAD_PATH = os.getenv("UPLOAD_PATH", "tmp/qa-data")

############### Number of log files ###############
LOGS_NUM = int(os.getenv("logs_num", "0"))

Minio_HOST = '152.136.174.19:9000'
Minio_ACCESS_KEY = 'admin'
Minio_SECRET_KEY = 'admin123'
