import json
import urllib

num_drug = 10

data = urllib.urlopen("https://api.fda.gov/drug/label.json?limit={}".format(num_drug)).read()
output = json.loads(data)

for i in range(num_drug):
    identificador = output['results'][i]['id']
    #nombre_medicamento = output['results'][i]['openfda']['generic_name'][0] No todos lo tienen
    print ("El identificador del medicamento {} es: {}".format(i, identificador))

