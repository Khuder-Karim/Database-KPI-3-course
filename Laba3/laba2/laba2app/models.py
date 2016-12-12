from __future__ import unicode_literals
import datetime

def Seller(fName, sName):
    return {
        "firstName": fName,
        "secondName": sName
    }

def Customer(fName, sName):
    return {
        "firstName": fName,
        "secondName": sName
    }

def Product(pName, price):
    return{
        "productName": pName,
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