from __future__ import unicode_literals
import datetime

def Seller(fName, lName, INNCode, legasy):
    return {
        "firstName": fName,
        "lastName": lName,
        "INNCode": INNCode,
        "legasy": legasy
    }

def Customer(fName, lName, region, city):
    return {
        "firstName": fName,
        "lastName": lName,
        "region": region,
        "city": city
    }

def Product(pName, pDesc, pBrand, price):
    return{
        "productName": pName,
        "productDesc": pDesc,
        "productBrand": pBrand,
        "price": price
    }

def Sale(seller, customer, product, amount, totalPrice):
    return {
        "seller": seller,
        "customer": customer,
        "product": product,
        "date": datetime.datetime.utcnow(),
        "amount": amount,
        "totalPrice": totalPrice
    }