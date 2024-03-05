class Redprint:
    def __init__(self, name):
        # name 是指视图类
        self.name = name
        # mound 是绑定路由方法 有多个
        self.mound = []

    # 重写路由 定义装饰器
    def route(self, rule, **options):
        def decorator(f):
            self.mound.append((f, rule, options))
            return f
        return decorator

    # 进行注册，传入蓝图和默认前缀
    def register(self, bp, url_prefix=None):
        if url_prefix is None:
            url_prefix = '/ '+ self.name
        for f, rule, options in self.mound:
            endpoint = options.pop("endpoint", f.__name__)
            bp.add_url_rule(url_prefix +rule, endpoint, f, **options)
            print(bp)


def prepare_for_json_return(sucess=True,data=None,error_msg=None):
    if not sucess and error_msg is None:
        raise ValueError("there is some wrong")
    return {"sucess":sucess,"data":data,"error_msg":error_msg}


