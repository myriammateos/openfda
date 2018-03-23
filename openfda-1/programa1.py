import json
import urllib

data = urllib.urlopen("https://api.fda.gov/drug/label.json").read()
output = json.loads(data)

identificador = output['results'][0]['id']
fabricante = output['results'][0]['openfda']['manufacturer_name'][0]
proposito = output['results'][0]['purpose'][0]

print ("El identificador es: {}".format(identificador))
print ("El proposito es: {}".format(proposito))
print ("El fabricante es: {}".format(fabricante))

