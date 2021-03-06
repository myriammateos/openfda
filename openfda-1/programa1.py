import json
import urllib.request

url = "https://api.fda.gov/drug/label.json"

try:
    data = urllib.request.urlopen(url).read().decode("utf-8")
    output = json.loads(data)
except urllib.error.URLError as error:
    print(error)
    print("La URL {} es erronea".format(url))
    exit(1)

identificador = output['results'][0]['id']
fabricante = output['results'][0]['openfda']['manufacturer_name'][0]
proposito = output['results'][0]['purpose'][0]

print("El identificador es: {}".format(identificador))
print("El proposito es: {}".format(proposito))
print("El fabricante es: {}".format(fabricante))


import goslate
gs = goslate.Goslate()
text = "Buenos días, ¿qué tal?"
print(gs.translate(text, 'es'))
