from flask import Flask
from flask import jsonify
from flask import request


import http.client
import json


def buscadorApi(url, ing, limit):
    web = "api.fda.gov"
    resource = "/drug/label.json"
    headers = {'User-Agent': 'http-client'}
    extra = url
    num_drug = limit

    if not 0 < num_drug <= 100:
        output = "Error, el numero de medicamentos debe estar entre 1 y 100"
        exit(1)

    conexion = http.client.HTTPSConnection(web)
    try:
        conexion.request("GET", resource + extra, None, headers)
    except http.client.socket.gaierror as error:
        print(error)
        print("Error de conexión, la URL {} no existe".format(web))
        exit(1)
    response = conexion.getresponse()
    if response.status != 200:
        output = "Error de conexión, el recurso solicitado {} no existe".format(resource)
        exit(1)

    data = response.read().decode("utf-8")
    conexion.close()
    output = json.loads(data)
    return output

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def getInicio():
    file_html = "indice.html"
    with open(file_html, "r") as f:
        message = f.read()
    return message

@app.route('/searchDrug', methods=['GET'])
def getDrug():
    numdrug = 10
    ingredient = request.args.get('active_ingredient', default = "*", type = str)
    limit = request.args.get('limit', default = numdrug, type = int)
    message = buscadorApi("/searchDrug?active_ingredient='{}'".format(ingredient),numdrug)
    return message

@app.route('/searchCompany', methods=['GET'])
def getCompany():
    page = request.args.get('company', default = "*", type = str)
    limit = request.args.get('limit', default = "10", type = int)
    return "Genial, estas buscando la empresa {}, el límite es {}".format(page,limit)

@app.route('/listDrugs',methods=['GET'])
def getListDrug():
    message = "Muestra la lista de farmacos"
    return message

@app.route('/listCompanies',methods=['GET'])
def getListCompanies():
    message = "Muestra la lista de empresas"
    return message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8800)