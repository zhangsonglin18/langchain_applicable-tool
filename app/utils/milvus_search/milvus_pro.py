import sys
import pandas as pd
from utils.embedding_pro.encode import SentenceModel
from config.configs import TOP_K, DEFAULT_TABLE
from utils.logs import LOGGER
from data_conn.milvus2.milvus_helpers import MilvusHelper
from data_conn.mysql8.mysql_helpers import MySQLHelper
class Milvus_pro:
    def __init__(self):
        self.milvus_cli = MilvusHelper
    def do_drop(self,table_name: str, milvus_cli: MilvusHelper, mysql_cli: MySQLHelper):
        if not table_name:
            table_name = DEFAULT_TABLE
        try:
            if not milvus_cli.has_collection(table_name):
                msg = f"Milvus doesn't have a collection named {table_name}"
                return msg
            status = milvus_cli.delete_collection(table_name)
            mysql_cli.delete_table(table_name)
            return status
        except Exception as e:
            LOGGER.error(f" Error with  drop table: {e}")
            sys.exit(1)

    def do_count(self,table_name: str, milvus_cli: MilvusHelper):
        if not table_name:
            table_name = DEFAULT_TABLE
        try:
            if not milvus_cli.has_collection(table_name):
                return None
            num = milvus_cli.count(table_name)
            return num
        except Exception as e:
            LOGGER.error(f" Error with count table {e}")
            sys.exit(1)


    def extract_features(self,file_dir, model):
        try:
            data = pd.read_csv(file_dir)
            question_data = data['question'].tolist()
            answer_data = data['answer'].tolist()
            sentence_embeddings = model.sentence_encode(question_data)
            return question_data, answer_data, sentence_embeddings
        except Exception as e:
            LOGGER.error(f" Error with extracting feature from question {e}")
            sys.exit(1)


    # Combine the id of the vector and the question data into a list
    def format_data(self,ids, question_data, answer_data):
        data = [(str(i), q, a) for i, q, a in zip(ids, question_data, answer_data)]
        return data


    # Import vectors to Milvus and data to Mysql respectively
    def do_load(self,table_name: str, file_dir: str, model: SentenceModel, milvus_client: MilvusHelper, mysql_cli: MySQLHelper):
        if not table_name:
            table_name = DEFAULT_TABLE
        if not milvus_client.has_collection(table_name):
            milvus_client.create_collection(table_name)
            milvus_client.create_index(table_name)
        question_data, answer_data, sentence_embeddings = self.extract_features(file_dir, model)
        ids = milvus_client.insert(table_name, sentence_embeddings)
        mysql_cli.create_mysql_table(table_name)
        mysql_cli.load_data_to_mysql(table_name, self.format_data(ids, question_data, answer_data))
        return len(ids)

    def do_search(self,table_name: str, question: str, model: SentenceModel, milvus_client: MilvusHelper, mysql_cli: MySQLHelper):
        try:
            if not table_name:
                table_name = DEFAULT_TABLE
            feat = model.sentence_encode([question])
            results = milvus_client.search_vectors(table_name, feat, TOP_K)
            vids = [str(x.id) for x in results[0]]
            questions = mysql_cli.search_by_milvus_ids(vids, table_name)
            distances = [x.distance for x in results[0]]
            return questions, distances
        except Exception as e:
            LOGGER.error(f" Error with search : {e}")
            sys.exit(1)


    def do_get_answer(self,table_name, question, mysql_cli):
        try:
            if not table_name:
                table_name = DEFAULT_TABLE
            answer = mysql_cli.search_by_question(question, table_name)
            return answer
        except Exception as e:
            LOGGER.error(f" Error with search by question : {e}")
            sys.exit(1)



