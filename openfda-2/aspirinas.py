import json
import urllib.request

num_drug = 100
active = "acetylsalicylic"
url = 'https://api.fda.gov/drug/label.json?search=active_ingredient:"{}"&limit={}'.format(active, num_drug)

try:
    data = urllib.request.urlopen(url).read().decode("utf-8")
    output = json.loads(data)
except urllib.error.URLError as error:
    if error.code == 404:
        print("Error 404, page not found")
    else:
        print("Another error occurred")
    print("La URL {} es erronea".format(url))
    exit(1)

print("Fabricantes de aspirinas:")
for i in range(len(output['results'])):
    if "manufacturer_name" in output['results'][i]['openfda'].keys():
        fabricante = output['results'][i]['openfda']['manufacturer_name'][0]
        print("  -" + fabricante)
    else:
        print("  -No especificado")

