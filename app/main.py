from flask import Flask, redirect,render_template, request
from api import api
from backend import controller as c
app = Flask (__name__)
app.template_folder = "frontend/templates"
app.static_folder = "frontend/static"

app.register_blueprint(api)

@app.route('/')
def _home_():
    return render_template('home.html')

@app.route('/search',methods=['GET'])
def _search_():
    return render_template('search.html',query = request.values.get('query'))

# @app.route('/listado',methods=['GET'])
# def _get_listado_():
#     # c.listar_palabras_cantidad()
#     c.backup()
#     return 'ok'

@app.route('/searched')
def _searched_():
    query = request.values.get('query')
    if query and query != 'None':
        return c._main_(query)
    else:
        return {'msg':'No se ha encontrado resultados'}

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5001, debug=True)