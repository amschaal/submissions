from lxml import etree
from xml.etree.ElementTree import tostring

tree = etree.parse("../Core.xsd")
NS = {"xs": "http://www.w3.org/2001/XMLSchema"}
# XPATH = "//xs:element[@name and .//xs:documentation]"
XPATH = "//xs:element[@name]"
elements = tree.xpath(XPATH,namespaces=NS)
element_map = {}
for el in elements:
    if el.attrib['name'] not in element_map or len(el) > element_map[el.attrib['name']]:
        element_map[el.attrib['name']] = el
#     print '-------------------'
#     print tostring(el)
print sorted(element_map.keys())

# print tostring(element_map['DataType'])
