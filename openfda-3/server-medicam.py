import http.server
import socketserver
import json
import urllib.request

# -- Puerto donde lanzar el servidor
PORT = 8000
IP = ""
num_drug = 10
url = "https://api.fda.gov/drug/label.json?limit={}".format(num_drug)

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        # Status
        self.send_response(200)

        # Que contenido estamos pasando
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Este es el mensaje que enviamos al cliente: un texto y
        # el recurso solicitado
        message = """<!doctype html>
                <html>
                  <body style='background-color:#1C1C1C'>
                    <font color="white">
                    <h1>LISTA DE MEDICAMENTOS</h2>"""

        data = urllib.request.urlopen(url).read().decode("utf-8")
        output = json.loads(data)

        message += """</p><table style="width:auto" class="width:egt" border="2">
                      <tr>
                        <th>Medicamento</th>
                        <th>Identificador</th>
                        <th>Principio activo</th>
                      </tr>"""

        for i in range(num_drug):
            try:
                name = output['results'][i]['openfda']['substance_name'][0]
            except KeyError:
                name = "No especificado"
            identificador = output['results'][i]['id']
            try:
                active = output['results'][i]['active_ingredient'][0]
            except KeyError:
                active = "No especificado"

            message += "<tr>"
            message += "<td>{}</th>".format(name)
            message += "<td>{}</th>".format(identificador)
            message += "<td>{}</th>".format(active)
            message += "</tr>"

        message += """</tr></tbody></table>
                    </font>
                    </body></html>"""

        # Enviar el mensaaje completo
        self.wfile.write(bytes(message, "utf8"))
        print("File served!")
        return


# ----------------------------------
# El servidor comienza a aqui
# ----------------------------------
# Establecemos como manejador nuestra propia clase
Handler = testHTTPRequestHandler

# -- Configurar el socket del servidor, para esperar conexiones de clientes
httpd = socketserver.TCPServer(("", PORT), Handler)
print("Serving at port", PORT)

# Entrar en el bucle principal
# Las peticiones se atienden desde nuestro manejador
# Cada vez que se ocurra un "GET" se invoca al metodo do_GET de
# nuestro manejador
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("")
    print("Interrumpido por el usuario")

print("")
print("Servidor parado")
httpd.server_close()
