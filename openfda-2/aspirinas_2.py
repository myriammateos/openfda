import http.client
import json

web = "api.fda.gov"
resource = "/drug/label.json"
headers = {'User-Agent': 'http-client'}
num_drug = 100
active = "acetylsalicylic"
extra = '?search=active_ingredient:"{}"&limit={}'.format(active,num_drug)
url = web + resource + extra

if not 0 < num_drug <= 100:
    print ("Error, el numero de medicamentos debe estar entre 1 y 100")
    exit(1)

conexion = http.client.HTTPSConnection(web)
try:
    conexion.request("GET", resource+extra, None, headers)
except:
    print("Error de conexión, la URL {} no existe".format(web))
    exit(1)
response = conexion.getresponse()
if response.status != 200:
    print("Error de conexión, la URL {} no existe".format(url))
    exit(1)

data = response.read().decode("utf-8")
conexion.close()

output = json.loads(data)

print("Fabricantes de aspirinas:")
for i in range(len(output['results'])):
    if "manufacturer_name" in output['results'][i]['openfda'].keys():
        fabricante = output['results'][i]['openfda']['manufacturer_name'][0]
        print("  -" + fabricante)
    else:
        print("  -No especificado")

