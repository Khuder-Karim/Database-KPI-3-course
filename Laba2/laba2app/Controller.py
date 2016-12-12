import json
from django.http import HttpResponse
from . database import Database
from bson import json_util

import redis

db = Database()

def getCustomer(request):
    customers = []
    for customer in db.getCustomer():
        customers.append(customer)

    return HttpResponse(json.dumps(customers, default=json_util.default), content_type='application/json')

def getSeller(request):
    sellers = []
    for seller in db.getSeller():
        sellers.append(seller)

    return HttpResponse(json.dumps(sellers, default=json_util.default), content_type='application/json')

def addSale(request):
    response = {}

    if request.method == "POST":
        response = db.addSale(json.loads(request.body, object_hook=json_util.object_hook))

    return HttpResponse(json.dumps(response, default=json_util.default), content_type="application/json")


def findSales(request):
    response = {}

    if request.method == "POST":
        response = db.findSales(json.loads(request.body, object_hook=json_util.object_hook))

    return HttpResponse(json.dumps(list(response), default=json_util.default), content_type="application/json")

def removeSale(request):
    if request.method == "POST":
        db.removeSale(json.loads(request.body, object_hook=json_util.object_hook))
    return HttpResponse(status=200)

def updateSale(request):
    response = {}
    if(request.method == "POST"):
        response = db.updateSale(json.loads(request.body, object_hook=json_util.object_hook))
    return HttpResponse(json.dumps(response, default=json_util.default), content_type="application/json")

def getSale(request):
    sales = []

    for sale in db.getSale():
        sales.append(sale)

    return HttpResponse(json.dumps(sales, default=json_util.default), content_type='application/json')

def getProduct(request):
    products = []

    for sale in db.getProduct():
        products.append(sale)

    return HttpResponse(json.dumps(products, default=json_util.default), content_type='application/json')

def restore(request):
    db.importFromCSV()
    return HttpResponse(json.dumps({"status": 200}), content_type="application/json")
