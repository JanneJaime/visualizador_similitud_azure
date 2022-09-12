from . import api
from flask import jsonify, request
from . import methods as mt


@api.route('/<string:query>',methods=['GET'])
def _api_get_(query):   
    obj = mt.start(query)
    return jsonify(obj),200,{'Content-Type': 'application/json'}