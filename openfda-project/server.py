# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
import http.client
import json
from flask import render_template, url_for, redirect

def buscadorApi(url, limit):
    web = "api.fda.gov"
    resource = "/drug/label.json"
    headers = {'User-Agent': 'http-client'}
    extra = url
    num_drug = limit
    output = "Correcto"

    if not 0 < num_drug <= 100:
        print("Error, el numero de medicamentos debe estar entre 1 y 100")
        code = "Error"
        return code

    conexion = http.client.HTTPSConnection(web)
    try:
        conexion.request("GET", resource + extra, None, headers)
    except http.client.socket.gaierror as error:
        print(error)
        print("Error de conexión, la URL {} no existe".format(web))
        code = "Error"
        return code

    response = conexion.getresponse()
    if response.status != 200:
        print("Error de conexión, el recurso solicitado {} no existe".format(resource+url))
        code = "Error"
        return code

    data = response.read().decode("utf-8")
    conexion.close()
    output = json.loads(data)
    return output

def searchDrug(output):
    solucion = []

    for i in range(len(output['results'])):
        if 'substance_name' in output['results'][i]['openfda'].keys():
            name = output['results'][i]['openfda']['substance_name'][0]
        else:
            name = "No especificado"
        if "manufacturer_name" in output['results'][i]['openfda'].keys():
            fabricante = output['results'][i]['openfda']['manufacturer_name'][0]
            url_enlace = 'http://127.0.0.1:8000/searchCompany?company={}'.format(fabricante.replace(" ", "+").replace(",", ""))
        else:
            url_enlace = "No especificado"
            fabricante = "No especificado"
        parejas = [name, url_enlace, fabricante]
        solucion.append(parejas)
    return solucion

def searchCompany(output):
    solucion = []
    for i in range(len(output['results'])):
        if 'substance_name' in output['results'][i]['openfda'].keys():
            name = output['results'][i]['openfda']['substance_name'][0]
        else:
            name = "No especificado"
        solucion.append(name)
    return solucion

def listDrug(output):
    solucion = []
    for i in range(len(output['results'])):
        if 'substance_name' in output['results'][i]['openfda'].keys():
            name = output['results'][i]['openfda']['substance_name'][0]
        else:
            name = "No especificado"
        solucion.append(name)
    return solucion

def listCompanies(output):
    solucion = []
    for i in range(len(output['results'])):
        if "manufacturer_name" in output['results'][i]['openfda'].keys():
            fabricante = output['results'][i]['openfda']['manufacturer_name'][0]
            url_enlace = 'http://127.0.0.1:8000/searchCompany?company={}'.format(fabricante.replace(" ", "+").replace(",",""))
        else:
            url_enlace = "No especificado"
            fabricante = "No especificado"
        parejas = [fabricante, url_enlace]
        solucion.append(parejas)
    return solucion

def listWarnings(output):
    solucion = []
    for i in range(len(output['results'])):
        if 'substance_name' in output['results'][i]['openfda'].keys():
            name = output['results'][i]['openfda']['substance_name'][0]
        else:
            name = "No especificado"
        if "warnings" in output['results'][i].keys():
            warning = output['results'][i]['warnings'][0]
        else:
            warning = "No especificado"
        parejas = [name, warning]
        solucion.append(parejas)
    return solucion

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def getInicio():
    return render_template("inicio.html")

@app.route('/searchDrug', methods=['GET'])
def getDrug():
    numdrug = 10
    ingredient = request.args.get('active_ingredient', default = "*", type = str)
    ingredient_searh = ingredient.replace(" ","+")
    limit = request.args.get('limit', default = numdrug, type = int)
    datos = buscadorApi('?search=active_ingredient:"{}"&limit={}'.format(ingredient_searh,limit), limit)
    if datos == "Error":
        return render_template("error.html")
    message = searchDrug(datos)
    return render_template("search_drug.html", content = message, active = ingredient)

@app.route('/searchCompany', methods=['GET'])
def getCompany():
    numdrug = 10
    empresa = request.args.get('company', default = "*", type = str)
    company_search = empresa.replace(" ", "+")
    limit = request.args.get('limit', default=numdrug, type=int)
    datos = buscadorApi('?search=manufacturer_name:"{}"&limit={}'.format(company_search, limit), limit)
    if datos == "Error":
        return render_template("error.html")
    message = searchCompany(datos)
    return render_template("search_company.html", content = message, company = empresa)

@app.route('/listDrugs', methods=['GET'])
def getListDrug():
    numdrug = 10
    limit = request.args.get('limit', default=numdrug, type=int)
    datos = buscadorApi('?limit={}'.format(limit), limit)
    if datos == "Error":
        return render_template("error.html")
    message = listDrug(datos)
    return render_template("list_drug.html", content = message)

@app.route('/listCompanies',methods=['GET'])
def getListCompanies():
    numdrug = 10
    limit = request.args.get('limit', default=numdrug, type=int)
    datos = buscadorApi('?limit={}'.format(limit), limit)
    if datos == "Error":
        return render_template("error.html")
    message = listCompanies(datos)
    return render_template("list_companies.html", content = message)

@app.route('/listWarnings',methods=['GET'])
def getListWarnings():
    numdrug = 10
    limit = request.args.get('limit', default=numdrug, type=int)
    datos = buscadorApi('?limit={}'.format(limit), limit)
    if datos == "Error":
        return render_template("error.html")
    message = listWarnings(datos)
    return render_template("list_warnings.html", content = message)

@app.route('/secret',methods=['GET'])
def secret():
    app.logger.error('Page not found: %s', (request.path))
    return render_template('error_401.html'), 401

@app.route('/redirect',methods=['GET'])
def redirigir():
    app.logger.error('Page not found: %s', (request.path))
    return redirect(url_for('getInicio'))

@app.errorhandler(404)
def page_not_found(e):
    app.logger.error('Page not found: %s', (request.path))
    return render_template('error_404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

