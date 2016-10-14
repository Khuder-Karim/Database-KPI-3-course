from lxml import etree as ET
data = ET.parse('data.xml').getroot()
print data.xpath('//page/@url')
