from lxml import etree as ET
from lxml import html as html

data = ET.Element("data")

root = html.parse('http://www.ostriv.in.ua/')

links = root.xpath("//a[contains(@href, 'ostriv.in.ua')]/@href")[0:20]
print len(links)
print links

for link in links:

    page = ET.SubElement(data, "page", url=link)

    p = html.parse(link)

    texts = p.xpath('//*[not(self::script) and not(self::style)][text()]')
    # fragment = ET.SubElement(page, "fragment", type="text")

    for text in texts:
        ET.SubElement(page, "fragment", type="text").text = text.text

    imgs = p.xpath('//img/@src')
    # fragment = ET.SubElement(page, "fragment", type="image")

    for img in imgs:
        ET.SubElement(page, "fragment", type="image").text = img

tree = ET.ElementTree(data)
tree.write("data.xml", pretty_print=True, encoding="UTF-8")
