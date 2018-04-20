class AceptConection():

    print("Estoy aquí")
    active = "{}".format(self.path[30:])
    print(active)
    print(self.path)
    extra = '?search=active_ingredient:"{}"&limit={}'.format(active, num_drug)
    conexion = http.client.HTTPSConnection(web)
    try:
        conexion.request("GET", resource + extra, None, headers)
    except http.client.socket.gaierror as error:
        print(error)
        print("Error de conexión, la URL {} no existe".format(web))
        exit(1)
    response = conexion.getresponse()
    if response.status != 200:
        print("Error de conexión, el recurso solicitado {} no existe".format(resource))
        exit(1)

    data = response.read().decode("utf-8")
    conexion.close()
    print(web + resource + extra)

    output = json.loads(data)
    #message = CrearPaginasHtml(extra).ShowHtml(data, 10)

    message = """<!doctype html>
                   <html>
                     <body style='background-color:#545454'>
                       <font color="white">
                       <h1>LISTA DE MEDICAMENTOS</h1>
                       <p>Medicamentos con el principio activo {}:</p>""".format(active)

    for i in range(len(output['results'])):
        if "generic_name" in output['results'][i]['openfda'].keys():
            medicamento = output['results'][i]['openfda']['generic_name'][0]

        else:
            medicamento = "No especificado"
        message += "<ul>{}</ul>".format(medicamento)

    message += """</font>
            </body></html>"""