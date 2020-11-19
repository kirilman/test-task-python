import csv, json
from xml.etree import ElementTree


def get_n(file_reader):
    l = list(filter(lambda x: x[0] == 'D', file_reader.fieldnames))
    return len(l)

def get_columns_names(file_reader):
    field = file_reader.fieldnames
    d_fields = list(filter(lambda x: x[0] == 'D', file_reader.fieldnames))
    m_fields = list(filter(lambda x: x[0] == 'M', file_reader.fieldnames))
    
    if len(d_fields) != len(m_fields):
        print('Dimensions of D,M are not equal')
        return d_fields + m_fields[:-1]
    return d_fields + m_fields

def preprocessing_csv_one(file_reader, n, fields, writer):
    for row in file_reader:
        insert_row = { field:row[field]for field in fields}
        writer.writerow(insert_row)
    
def preprocessing_csv_two(file_reader, n, fields, writer):
    for row in file_reader:
        insert_row = {field:row[field] for field in fields}
        writer.writerow(insert_row)
    
def preprocessing_json_file(data, fields, writer):
    for row in data['fields']:
        insert_row = { key:row[key] for key in fields}
        writer.writerow(insert_row)    
        
def preprocessing_xml_file(file_name, fields, writer):
    tree = ElementTree.parse(file_name)
    root = tree.getroot()
    objects = root.getchildren()
    objects = root.findall("objects")
    for obj in objects:
        insert_row = {item.attrib['name']: item.find('value').text for item in obj}
        writer.writerow(insert_row)