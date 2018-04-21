from flask import Flask
from flask import request
import http.client
import json


def buscadorApi(url, limit):
    web = "api.fda.gov"
    resource = "/drug/label.json"
    headers = {'User-Agent': 'http-client'}
    extra = url
    num_drug = limit
    print(url)
    print(web + resource + url)

    if not 0 < num_drug <= 100:
        print("Error, el numero de medicamentos debe estar entre 1 y 100")
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
        print("Error de conexión, el recurso solicitado {} no existe".format(resource+url))
        exit(1)

    data = response.read().decode("utf-8")
    conexion.close()
    output = json.loads(data)
    return output

def searchDrug(output, medicament):
    solucion = "<p> Medicamentos que contienen {}: </p>".format(medicament)
    for i in range(len(output['results'])):
        if 'substance_name' in output['results'][i]['openfda'].keys():
            name = output['results'][i]['openfda']['substance_name'][0]
        else:
            name = "No especificado"
        if "manufacturer_name" in output['results'][i]['openfda'].keys():
            fabricante = output['results'][i]['openfda']['manufacturer_name'][0]
        else:
            fabricante = "No especificado"
        solucion += "<ul>Medicamento: {}</ul>".format(name)
        solucion += "<ul>Fabricante: {}</ul>".format(fabricante)
    return solucion

def searchCompany(output, company):
    solucion = "<p> Medicamentos de la empresa {}: </p>".format(company)
    for i in range(len(output['results'])):
        if 'substance_name' in output['results'][i]['openfda'].keys():
            name = output['results'][i]['openfda']['substance_name'][0]
        else:
            name = "No especificado"
        solucion += "<ul>{}</ul>".format(name)
    return solucion

def listDrug(output):
    solucion = "<p> Lista de medicamento:</p>"
    for i in range(len(output['results'])):
        if 'substance_name' in output['results'][i]['openfda'].keys():
            name = output['results'][i]['openfda']['substance_name'][0]
        else:
            name = "No especificado"
        solucion += '<ul>{}</ul>'.format(name)
    return solucion

def listCompanies(output):
    solucion = "<p> Lista de fabricantes:</p>"
    for i in range(len(output['results'])):
        if "manufacturer_name" in output['results'][i]['openfda'].keys():
            fabricante = output['results'][i]['openfda']['manufacturer_name'][0]
            url_enlace = 'http://127.0.0.1:8000/searchCompany?company={}'.format(fabricante.replace(" ", "+").replace(",",""))
            print(url_enlace)
            mostrar = '<a href="{}">{}</a>'.format(url_enlace, fabricante)
        else:
            mostrar = "No especificado"
        solucion += '<ul>{}</ul>'.format(mostrar)
    return solucion

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
    ingredient_searh = ingredient.replace(" ","+")
    limit = request.args.get('limit', default = numdrug, type = int)
    datos = buscadorApi('?search=active_ingredient:"{}"&limit={}'.format(ingredient_searh,limit), limit)
    message = searchDrug(datos,ingredient)
    return message

@app.route('/searchCompany', methods=['GET'])
def getCompany():
    numdrug = 10
    company = request.args.get('company', default = "*", type = str)
    company_search = company.replace(" ", "+")
    limit = request.args.get('limit', default=numdrug, type=int)
    datos = buscadorApi('?search=manufacturer_name:"{}"&limit={}'.format(company_search, limit), limit)
    message = searchCompany(datos, company)
    return message

@app.route('/listDrugs',methods=['GET'])
def getListDrug():
    numdrug = 10
    limit = request.args.get('limit', default=numdrug, type=int)
    datos = buscadorApi('?limit={}'.format(limit), limit)
    message = listDrug(datos)
    return message

@app.route('/listCompanies',methods=['GET'])
def getListCompanies():
    numdrug = 10
    limit = request.args.get('limit', default=numdrug, type=int)
    datos = buscadorApi('?limit={}'.format(limit), limit)
    message = listCompanies(datos)
    return message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)