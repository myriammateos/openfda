import http.client
import json

web = "api.fda.gov"
resource = "/drug/label.json"
headers = {'User-Agent': 'http-client'}
num_drug = 100
active = "acetylsalicylic"
extra = '?search=active_ingredient:"{}"&limit={}'.format(active,num_drug)

conexion = http.client.HTTPSConnection(web)
conexion.request("GET", resource+extra, None, headers)
response = conexion.getresponse()

data = response.read().decode("utf-8")
conexion.close()

output = json.loads(data)

print("Fabricantes de aspirinas:")
for i in range(len(output['results'])):
    try:
        fabricante = output['results'][i]['openfda']['manufacturer_name'][0]
        print("  -" + fabricante)
    except KeyError:
        print("  -No especificado")