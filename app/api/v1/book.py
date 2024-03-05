from app.api.v1 import bp_v1 as blueprint

@blueprint.post('/get')
def get_user():
    return "I am book get method"

@blueprint.post('/create')
def get_book():
    return "create book method"