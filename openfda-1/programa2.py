import json
import urllib

num_drug = 10

data = urllib.urlopen("https://api.fda.gov/drug/label.json?limit={}".format(num_drug)).read()
output = json.loads(data)

for i in range(num_drug):
    identificador = output['results'][i]['id']
    print ("El identificador del medicamento numero {} es: {}".format(i, identificador))
