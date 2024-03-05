from flask import Blueprint
bp_v1 = Blueprint('v1',__name__,url_prefix="/v1")
from app.api.v1 import user, book