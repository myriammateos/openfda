import json
import urllib.request

num_drug = 10
url = "https://api.fda.gov/drug/label.json?limit={}".format(num_drug)

data = urllib.request.urlopen(url).read().decode("utf-8")
output = json.loads(data)

for i in range(num_drug):
    identificador = output['results'][i]['id']
    print ("El identificador del medicamento {} es: {}".format(i, identificador))

