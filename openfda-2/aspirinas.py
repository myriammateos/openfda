import json
import urllib


num_drug = 100
active = "acetylsalicylic"

data = urllib.urlopen('https://api.fda.gov/drug/label.json?search=active_ingredient:"{}"&limit={}'.format(active,num_drug)).read()
output = json.loads(data)

print("Fabricantes de aspirinas:")
for i in range(len(output['results'])):
    try:
        fabricante = output['results'][i]['openfda']['manufacturer_name'][0]
        print(fabricante)
    except KeyError:
        print("No especificado")
