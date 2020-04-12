from xml.etree import ElementTree


tree = ElementTree.parse("sitemap.xml")
root = tree.getroot()

print(root)
print(root.tag)
print(root.attrib)

url_list = []
for child in root:
    for c in child:
        url = c.text[8:]
        url_list.append(str(url))

url_list.sort()

for u in url_list:
    print(u)



# for element in root.iter("urlset"):
#     print(element)
