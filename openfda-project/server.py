from flask import Flask
from flask import request
import http.client
import json
from flask import render_template

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
    solucion = []

    for i in range(len(output['results'])):
        if 'substance_name' in output['results'][i]['openfda'].keys():
            name = output['results'][i]['openfda']['substance_name'][0]
        else:
            name = "No especificado"
        if "manufacturer_name" in output['results'][i]['openfda'].keys():
            fabricante = output['results'][i]['openfda']['manufacturer_name'][0]
            url_enlace = 'http://127.0.0.1:8000/searchCompany?company={}'.format(fabricante.replace(" ", "+").replace(",", ""))
            print(url_enlace)
        else:
            url_enlace = "No especificado"
            fabricante = "No especificado"
        parejas = [name, url_enlace, fabricante]
        solucion.append(parejas)
    return solucion

def searchCompany(output, company):
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
        parejas = [fabricante, url_enlace]
        solucion.append(parejas)
        print(solucion)
    return solucion

def htmlizador(cuerpo):
    encabezado = "<!DOCTYPE html>"
    encabezado += '<html lang = "en">'
    encabezado += "<head>"
    encabezado += '<meta charset = "UTF-8">'
    encabezado += "<title>{}</title>".format("Poner título")
    encabezado += '<link rel = "stylesheet" type= "text/css" href="static/plantilla.css"'
    encabezado += "</head>"
    encabezado += "<body>"
    final = "</body></html>"
    return encabezado + cuerpo + final


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
    message = searchDrug(datos,ingredient)
    return render_template("search_drug.html", content = message, active = ingredient)

@app.route('/searchCompany', methods=['GET'])
def getCompany():
    numdrug = 10
    empresa = request.args.get('company', default = "*", type = str)
    company_search = empresa.replace(" ", "+")
    limit = request.args.get('limit', default=numdrug, type=int)
    datos = buscadorApi('?search=manufacturer_name:"{}"&limit={}'.format(company_search, limit), limit)
    message = searchCompany(datos, empresa)
    return render_template("search_company.html", content = message, company = empresa)

@app.route('/listDrugs',methods=['GET'])
def getListDrug():
    numdrug = 10
    limit = request.args.get('limit', default=numdrug, type=int)
    datos = buscadorApi('?limit={}'.format(limit), limit)
    message = listDrug(datos)
    return render_template("list_drug.html", content = message)

@app.route('/listCompanies',methods=['GET'])
def getListCompanies():
    numdrug = 10
    limit = request.args.get('limit', default=numdrug, type=int)
    datos = buscadorApi('?limit={}'.format(limit), limit)
    message = listCompanies(datos)
    return render_template("list_companies.html", content = message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
