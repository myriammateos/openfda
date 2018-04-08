import http.client
import json

web = "api.fda.gov"  # -- Nombre del servidor REST
resource = "/drug/label.json"
headers = {'User-Agent': 'http-client'}
url = web + resource

conexion = http.client.HTTPSConnection(web)

try:
    conexion.request("GET", resource, None, headers)
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

identificador = output['results'][0]['id']
fabricante = output['results'][0]['openfda']['manufacturer_name'][0]
proposito = output['results'][0]['purpose'][0]

print("El identificador es: {}".format(identificador))
print("El proposito es: {}".format(proposito))
print("El fabricante es: {}".format(fabricante))
