from lxml import etree as ET
from lxml import html as html

def join (array, separator):
    str = ""
    for item in array:
        str = str + item + separator
    return str

page = html.parse('http://www.fishing-mart.com.ua/')

data = ET.Element("data")

categories = page.xpath("//div[@class='block_content']/ul[contains(@class, 'tree')]/li/ul/li/a/@href")[0:17]

for cat in categories:

    categoriesElement = ET.SubElement(data, 'category', url=cat)

    p = html.parse(cat)

    products = p.xpath("//ul[@id='product_list']/li/*/a[@class='product_img_link']/@href")

    for pr in products:
        productElement = ET.SubElement(categoriesElement, "product", url=pr)

        p = html.parse(pr)

        #Print Header
        header = p.xpath("//div[@id='primary_block']/h1/text()")[0]
        ET.SubElement(productElement, 'header', type="text").text = header

        #print Image
        image = p.xpath("//div[@id='primary_block']//img[@id='bigpic']/@src")[0]
        ET.SubElement(productElement, 'image', type="image").text = image

        #print price
        price = p.xpath("//div[@id='primary_block']//span[@id='our_price_display']/text()")[0]
        ET.SubElement(productElement, 'price', type="text").text = price

        #print description
        desc = join(p.xpath("//div[@id='more_info_sheets']/div[@id='idTab1']//text()"), " ")
        ET.SubElement(productElement, 'description', type="text").text = desc

tree = ET.ElementTree(data)
tree.write("data-3.xml", pretty_print=True, encoding="UTF-8")

