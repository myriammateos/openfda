import json
import urllib.request


num_drug = 100
active = "acetylsalicylic"

data = urllib.request.urlopen('https://api.fda.gov/drug/label.json?search=active_ingredient:"{}"&limit={}'.format(active,num_drug)).read().decode("utf-8")
output = json.loads(data)

print("Fabricantes de aspirinas:")
for i in range(len(output['results'])):
    try:
        fabricante = output['results'][i]['openfda']['manufacturer_name'][0]
        print("  -" + fabricante)
    except KeyError:
        print("  -No especificado")

