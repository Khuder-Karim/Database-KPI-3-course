"""Laba2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from laba2app import Controller as mc
from laba2app import views as v

urlpatterns = [
    # url(r'^search', mc.search),
    # url(r'^by_legasy', mc.filterByLegasy),
    url(r'^restore', mc.restore),
    url(r'^customer', mc.getCustomer),
    # url(r'^loaddata', mc.loaddata),
    url(r'^admin/', admin.site.urls),
    url(r'^sale/add', mc.addSale),
    url(r'^sale/remove', mc.removeSale),
    url(r'^sale/update', mc.updateSale),
    url(r'^sale', mc.getSale),
    url(r'^seller', mc.getSeller),
    url(r'^product', mc.getProduct),

    # url(r'^sale/update', mc.updateSale),
    # url(r'^sale/delete', mc.deleteSale),
    url('', v.index),
]
