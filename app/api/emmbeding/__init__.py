from flask import Blueprint
emd_v1 = Blueprint('emd',__name__,url_prefix="/emd")
from app.api.emmbeding import emb_api