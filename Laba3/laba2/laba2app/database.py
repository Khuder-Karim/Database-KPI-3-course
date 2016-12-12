# -*- coding: utf-8 -*-

from pymongo import MongoClient
import csv
import models
from bson.code import Code
from random import randint
from bson.objectid import ObjectId
import time
import redis, json
from bson import json_util

class Database:
    def __init__(self):
        self.client = MongoClient()
        # self.client.drop_database("saleDB")
        self.db = self.client["saleDB"]
        self.customers = self.db["Customers"]
        self.products = self.db["Products"]
        self.sellers = self.db["Sellers"]
        self.sales = self.db["Sales"]

        self.redis = redis.Redis()

        # self.setData()


    def importFromCSV(self):
        self.client.drop_database("saleDB")

    def setData(self):
        womens = ["Myrtis Kahn  ", "Margery Hou  ", "Georgianne Teneyck  ", "Zora Dunsmore  ", "Misha Calcagni  ", "Coral Watson  ", "Destiny Millet  ", "Willodean Severt  ", "Nanci Nicol  ", "Maris Credle  ", "Brittney Hawes  ", "Maryrose Butterworth  ", "Catherin Dobson  ", "Marylin Torpey  ", "Myrtle Tracy  ", "Velda Coy  ", "Lolita Maglio  ", "Stephaine Ciulla  ", "Regina Quarterman  ", "Dorine Bucy  "]
        mans = ["Lowell Wightman  ", "Avery Harriger  ", "Alonso Marcello  ", "Johnson Rego  ", "Wilfred Mackay  ", "Trent Dimick  ", "Edgar Holtkamp  ", "Nicholas Chaudhry  ", "Bernard Bourbeau  ", "Gabriel Sperling  ", "Rolf Cirillo  ", "Ruben Turberville  ", "Ethan Dresser  ", "Spencer Bourque  ", "Marcelo Draves  ", "Galen Maybee  ", "Malcom Mckee  ", "Felix Moreles  ", "Reuben Villalpando  ", "Archie Liao  "]
        sellers = []
        products = []
        customers = []
        for p in womens:
            sellers.append(self.sellers.insert_one(models.Seller(p.split(" ")[0], p.split(" ")[1])).inserted_id)
            customers.append(self.customers.insert_one(models.Customer(p.split(" ")[0], p.split(" ")[1])).inserted_id)
        for p in mans:
            sellers.append(self.sellers.insert_one(models.Seller(p.split(" ")[0], p.split(" ")[1])).inserted_id)
            customers.append(self.customers.insert_one(models.Customer(p.split(" ")[0], p.split(" ")[1])).inserted_id)
        for i in range(0, 100):
            products.append(self.products.insert_one(models.Product("Product "+str(randint(0, 1000)), randint(0, 10000))).inserted_id)

        for i in range(0, 75000):
            pr = self.products.find_one({'_id': ObjectId(products[randint(0, len(products)-1)])})
            count = randint(0, 10)

            sell = self.sellers.find_one({"_id": sellers[randint(0, len(sellers)-1)]})
            cust = self.customers.find_one({"_id": customers[randint(0, len(customers)-1)]})

            self.sales.insert_one(models.Sale( sell, cust, pr, count, count*pr["price"] ))

    def getCustomer(self):
        return self.customers.find()

    def getSeller(self):
        return self.sellers.find()

    def getProduct(self):
        return self.products.find()

    def addSale(self, req):
        sale_id = self.sales.insert_one(models.Sale(**req)).inserted_id
        return self.sales.find_one({"_id": sale_id})

    def removeSale(self, req):
        self.sales.delete_one({"_id": req["_id"]})

    def updateSale(self, req):
        self.removeSale(req)
        sale_id = self.sales.insert_one(models.Sale(req["seller"], req["customer"], req["product"], req["amount"], req["totalPrice"])).inserted_id
        return self.sales.find_one({"_id": sale_id})

    def getSale(self):
        return self.sales.find().limit(50)

    def findSales(self, req):
        with Profiler() as p:
            if self.redis.exists(req["idProduct"]) == 1:
                return json.loads(self.redis.get(req["idProduct"]))

            response =  list(self.sales.find({ "product._id": ObjectId(req["idProduct"]) }).limit(100))
            self.redis.set(req["idProduct"], json.dumps(response, default=json_util.default))

            return response

    def stat(self):
        map1 = Code("""
                        function() {
                            emit(this.customer._id, this.totalPrice)
                        }
                """)

        reduce1 = Code("""
                        function(key, values) {
                            var sum = 0;
                            for(var i in values) {
                                sum += values[i];
                            }
                            return sum;
                        }
                """)

        s1 = self.sales.map_reduce(map1, reduce1, "Total price for every customer").find()

        print "-" * 40
        print "How much spent every customer on this resource\n"
        for s in s1:
            print s
        print "-" * 40

    def stat_2(self):
        map2 = Code("""
                                function() {
                                    emit(this.seller._id, this.amount)
                                }
                        """)

        reduce2 = Code("""
                                function(key, values) {
                                    var sum = 0;
                                    for(var i in values) {
                                        sum += +values[i];
                                    }
                                    return sum;
                                }
                        """)

        s2 = self.sales.map_reduce(map2, reduce2, "Count of big sale").find()

        print "-" * 40
        print "Колиество проданных продуктов для каждого продавца\n"
        for s in s2:
            print s
        print "-" * 40

    def stat_3(self):
        s2 = self.sales.aggregate(
            [
                {"$project": {"_id": 0, "seller": "$seller.firstName", "product": "$product.productName", "price": "$totalPrice"}},
                {"$group": {"_id": {"seller": "$seller", "product": "$product"}, "price": {"$sum": "$price"}}},
                {"$sort": {"price": +1}},
                {"$group": {"_id": "$_id.seller", "products": {"$addToSet": {"product": "$_id.product", "totalPrice": "$price"}}}},
                # {"$unwind": "$products"},
                {"$project": {"item": {"$arrayElemAt": ["$products", 0]}}}
            ]
        )

        print "-" * 40
        print "Лучшие покупатели каждого продукта \n"
        for s in s2:
            print s
        print "-" * 40

db = Database()
# db.stat()
# db.stat_2()
# db.stat_3()

class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self, type, value, traceback):
        print "Elapsed time: {:.3f} sec".format(time.time() - self._startTime)