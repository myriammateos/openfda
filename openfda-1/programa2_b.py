import http.client
import json

web = "api.fda.gov"  # -- Nombre del servidor REST
resource = "/drug/label.json"
headers = {'User-Agent': 'http-client'}
num_drug = 10
limit = "?limit={}".format(num_drug)
url = web + resource

conexion = http.client.HTTPSConnection(web)
conexion.request("GET", resource+limit, None, headers)
response = conexion.getresponse()
if response.status != 200:
    print("Error de conexión, la URL {} no existe".format(url))
    exit(1)

data = response.read().decode("utf-8")
conexion.close()

output = json.loads(data)
for i in range(num_drug):
    identificador = output['results'][i]['id']
    print ("El identificador del medicamento {} es: {}".format(i, identificador))

