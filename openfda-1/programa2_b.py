import http.client
import json

web = "api.fda.gov"  # -- Nombre del servidor REST
resource = "/drug/label.json"
headers = {'User-Agent': 'http-client'}
num_drug = 10
limit = "?limit={}".format(num_drug)


conexion = http.client.HTTPSConnection(web)
conexion.request("GET", resource+limit, None, headers)
response = conexion.getresponse()

data = response.read().decode("utf-8")
conexion.close()

output = json.loads(data)
for i in range(num_drug):
    identificador = output['results'][i]['id']
    print ("El identificador del medicamento {} es: {}".format(i, identificador))

