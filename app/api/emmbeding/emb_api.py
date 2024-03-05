from flask import request
import json
from app.api.emmbeding import emd_v1 as blueprint
from app.api.emmbeding.utils import text_decoding
from app.libs import prepare_for_json_return


@blueprint.route('/get_text_embeding',methods=['POST'])
def get_text_embeding():
    data = request.json.get("text")
    bedding = text_decoding(data).tolist()
    return prepare_for_json_return({"data":bedding})
