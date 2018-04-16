import http.server
import socketserver
import json
import http.client
import os

# Info
web = "api.fda.gov"
resource = "/drug/label.json"
headers = {'User-Agent': 'http-client'}
PORT = 8000
IP = ""  # Por defecto coge la IP local 127.0.0.1
num_drug = 10
extra = '?limit={}'.format(num_drug)
url = web + resource + extra
socketserver.TCPServer.allow_reuse_address = True

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
    print("Error de conexión, el recurso solicitado {} no existe".format(resource))
    exit(1)

data = response.read().decode("utf-8")
conexion.close()

output = json.loads(data)

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        # Status
        self.send_response(200)

        # Que contenido estamos pasando
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Este es el mensaje que enviamos al cliente: un texto y el recurso solicitado

        solicitud = self.path[1:]

        if self.path == "/":
            file_html = "indice.html"

        with open(file_html, "r") as f:
            message = f.read()


        #message =

        # Enviar el mensaaje completo
        self.wfile.write(bytes(message, "utf8"))
        print("File served!")
        return

# ----------------------------------
# El servidor comienza a aqui
# ----------------------------------

# Establecemos como manejador nuestra propia clase
Handler = testHTTPRequestHandler

# Configurar el socket del servidor, para esperar conexiones de clientes
httpd = socketserver.TCPServer(("", PORT), Handler)
print("Serving at port", PORT)

# Entrar en el bucle principal
# Las peticiones se atienden desde nuestro manejador
# Cada vez que se ocurra un "GET" se invoca al metodo do_GET de nuestro manejador
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("")
    print("Interrumpido por el usuario")

print("")
print("Servidor parado")
httpd.server_close()
