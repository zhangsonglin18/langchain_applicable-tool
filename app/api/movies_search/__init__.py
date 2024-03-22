from flask import Blueprint
mv_v1 = Blueprint('movies_search',__name__,url_prefix="/mv_search")
from app.api.movies_search import mvilvus_search