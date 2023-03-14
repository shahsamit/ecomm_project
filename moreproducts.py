import requests
import json

def getproducts():
	url = "https://fakestoreapi.com/products"
	response = requests.get(url)
	y = json.loads(response.text)
	return y
#for a in y:
#	print(a["image"])

#print(getproducts())
