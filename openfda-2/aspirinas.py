import json
import urllib


num_drug = 100

data = urllib.urlopen('https://api.fda.gov/drug/label.json?search=active_ingredient:"acetylsalicylic%22&limit=100').read()
output = json.loads(data)

for i in range(num_drug):
    fabricante = output['results'][i]['openfda']['manufacturer_name'][0]
    print(fabricante)