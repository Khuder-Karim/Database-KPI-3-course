# -*- coding: utf-8 -*-

from pymongo import MongoClient
import csv
import models
from bson.code import Code

class Database:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client["saleDB"]
        self.customers = self.db["Customers"]
        self.products = self.db["Products"]
        self.sellers = self.db["Sellers"]
        self.sales = self.db["Sales"]

    def importFromCSV(self):
        self.client.drop_database("saleDB")

        with open('./laba2app/static/product.csv', 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                self.products.insert_one(models.Product(*row))
        with open('./laba2app/static/customer.csv', 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                self.customers.insert_one(models.Customer(*row))
        with open('./laba2app/static/seller.csv', 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                self.sellers.insert_one(models.Seller(*row))

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
        return self.sales.find()

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

