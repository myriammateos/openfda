import http.client
import json

web = "api.fda.gov"
resource = "/drug/label.json"
headers = {'User-Agent': 'http-client'}
num_drug = 10
limit = "?limit={}".format(num_drug)
url = web + resource

if not 0 < num_drug <= 100:
    print ("Error, el numero de medicamentos debe estar entre 1 y 100")
    exit(1)

conexion = http.client.HTTPSConnection(web)

try:
    conexion.request("GET", resource+limit, None, headers)
except http.client.socket.gaierror as error:
    print(error)
    print("Error de conexión, la URL {} no existe".format(web))
    exit(1)
response = conexion.getresponse()
if response.status != 200:
    print("Error de conexión, el recurso {} no existe".format(resource))
    exit(1)

data = response.read().decode("utf-8")
conexion.close()

output = json.loads(data)
for i in range(num_drug):
    identificador = output['results'][i]['id']
    print ("El identificador del medicamento {} es: {}".format(i+1, identificador))

