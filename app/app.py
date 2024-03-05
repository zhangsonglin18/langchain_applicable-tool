from flask import Flask

def register_blueprints(app):
    from app.api.v1 import bp_v1
    app.register_blueprint(bp_v1, url_prefix='/v1')
    from app.api.emmbeding import emd_v1
    app.register_blueprint(emd_v1, url_prefix='/emd')

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')
    # 解决跨域问题
    from flask_cors import CORS
    cors = CORS()
    cors.init_app(app, resources={"/*": {"origins": "*"}})
    # 将蓝图注册到app 上
    register_blueprints(app)
    return app