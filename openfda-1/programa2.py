import json
import urllib.request

num_drug = 10
url = "https://api.fda.gov/drug/label.json?limit={}".format(num_drug)

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

for i in range(num_drug):
    identificador = output['results'][i]['id']
    print ("El identificador del medicamento {} es: {}".format(i, identificador))

