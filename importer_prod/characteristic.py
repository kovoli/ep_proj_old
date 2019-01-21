import xmltodict, json
import pprint


xml = """
<offer>
<param name="Вес" unit="г">4495</param>
<param name="Ширина упаковки" unit="мм">540</param>
<param name="Высота упаковки" unit="мм">140</param>
<param name="Глубина упаковки" unit="мм">490</param>
<param name="Тип">Вентилятор</param>
<param name="Год выпуска">2013</param>
<param name="Комплектация">Вентилятор, пульт ДУ, инструкция</param>
<param name="Мощность" unit="Вт">50 Вт</param>
<param name="Макс. площадь помещения" unit="квм">30 кв. м</param>
<param name="Установка">Напольная</param>
</offer>
"""


#pp = pprint.PrettyPrinter(indent=2)
#pp.pprint(json.dumps(xmltodict.parse(xml), ensure_ascii=False))

asd = {'param': [{'name': 'Вес', 'unit': 'г', 'text': 4495},
       {'name': 'Ширина упаковки', 'unit': 'мм', 'text': 555}]}

#print(asd['name'])
for i, j in asd.items():
    print(i, j[j])