from configparser import ConfigParser
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