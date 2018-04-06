import http.client
import json

web = "api.fda.gov"  # -- Nombre del servidor REST
resource = "/drug/label.json"
headers = {'User-Agent': 'http-client'}

conexion = http.client.HTTPSConnection(web)
conexion.request("GET", resource, None, headers)
response = conexion.getresponse()

data = response.read().decode("utf-8")
conexion.close()

output = json.loads(data)

identificador = output['results'][0]['id']
fabricante = output['results'][0]['openfda']['manufacturer_name'][0]
proposito = output['results'][0]['purpose'][0]

print("El identificador es: {}".format(identificador))
print("El proposito es: {}".format(proposito))
print("El fabricante es: {}".format(fabricante))
