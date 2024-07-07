import xml.etree.ElementTree as ET

def process_xml(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    seen_types = set()

    for type_element in list(root):
        type_name = type_element.attrib.get('name')
        if type_name in seen_types:
            root.remove(type_element)
            continue
        seen_types.add(type_name)

        nominal = type_element.find('nominal')
        if nominal is not None and nominal.text == '0':
            for child in list(type_element):
                if child.tag not in ['nominal', 'lifetime', 'flags']:
                    type_element.remove(child)
        elif nominal is not None and int(nominal.text) > 0:
            continue
        else:
            root.remove(type_element)

    # Создаем новый файл с необходимыми форматами
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        file.write('<types>\n')
        for type_element in root:
            file.write('  <type name="{}">\n'.format(type_element.attrib['name']))
            for child in type_element:
                if child.tag == 'flags':
                    # Пишем атрибуты flags с сохранением значений 0 или 1
                    file.write('    <flags count_in_cargo="{}" count_in_hoarder="{}" count_in_map="{}" count_in_player="{}" crafted="{}" deloot="{}" />\n'.format(
                        child.attrib.get('count_in_cargo', '0'),
                        child.attrib.get('count_in_hoarder', '0'),
                        child.attrib.get('count_in_map', '0'),
                        child.attrib.get('count_in_player', '0'),
                        child.attrib.get('crafted', '0'),
                        child.attrib.get('deloot', '0')
                    ))
                elif child.tag == 'category':
                    file.write('    <category name="{}" />\n'.format(child.attrib['name']))
                elif child.tag == 'value':
                    file.write('    <value name="{}" />\n'.format(child.attrib['name']))
                elif child.tag == 'usage':
                    file.write('    <usage name="{}" />\n'.format(child.attrib['name']))
                else:
                    file.write('    <{}>{}</{}>\n'.format(child.tag, child.text if child.text is not None else '', child.tag))
            file.write('  </type>\n')
        file.write('</types>\n')

# Пример использования
process_xml('types.xml', 'processed_types.xml')
