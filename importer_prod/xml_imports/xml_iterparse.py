import xml.etree.ElementTree as etree
con = 0
for event, elem in etree.iterparse('10500.xml', events=('start',)):
    if elem.tag == 'offer':
        for i in elem:
            a = {}
            if i.tag == 'oldprice':
                con += 1

    elem.clear()
print(con)