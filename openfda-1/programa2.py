import json
import urllib.request

num_drug = 10
url = "https://api.fda.gov/drug/label.json?limit={}".format(num_drug)

if not 0 < num_drug <= 100:
    print ("Error, el numero de medicamentos debe estar entre 1 y 100")
    exit(1)

try:
    data = urllib.request.urlopen(url).read().decode("utf-8")
    output = json.loads(data)
except urllib.error.URLError as error:
    print(error)
    print("La URL {} es erronea".format(url))
    exit(1)

for i in range(num_drug):
    identificador = output['results'][i]['id']
    print("El identificador del medicamento {} es: {}".format(i+1, identificador))


