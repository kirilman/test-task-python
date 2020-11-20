import csv, json
from xml.etree import ElementTree
import os

def get_n(file_reader):
    l = list(filter(lambda x: x[0] == 'D', file_reader.fieldnames))
    return len(l)

def get_columns_names(file_reader):
    """
        Получить имена столбцов из первого csv файла
    """
    field = file_reader.fieldnames
    d_fields = list(filter(lambda x: x[0] == 'D', file_reader.fieldnames))
    m_fields = list(filter(lambda x: x[0] == 'M', file_reader.fieldnames))
    
    if len(d_fields) != len(m_fields):
        print('Dimensions of D,M are not equal')
        return d_fields + m_fields[:len(d_fields)]
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

def sort_resulting_file(inpt_file_name, out_file_name):
    """
        Сортировка файла по первому столбцу
    """
    file = open(inpt_file_name, 'r')
    lines = file.readlines()
    head = lines[0]
    lines = lines[1:]
    file.close()
    
    first_row = []
    for line in lines:
        s = line.split(',')[0]
        first_row.append(s)   
    indx = [e[0] for e in sorted(enumerate(first_row), key = lambda x:x[1])]
    
    #перекладываем в новый список
    new_list = [None for i in range(len(first_row))]
    for i, s in enumerate(indx):
        new_list[i] = lines[s]
        
    file = open(out_file_name, 'w')
    file.write(head.replace(',','\t'))
    for line in new_list:
        file.write(line.replace(',','\t'))
    file.close()    
    os.remove(inpt_file_name)

def group_result_file(result_filename, result_group_filename, n):
    """
        Сумма значений по сгруппированным комбинациям
        Advanced_result
    """
    file = open(result_filename,'r')
    lines = file.readlines()
    head = lines[0].replace('\n','').split('\t')
    lines = lines[1:]
    file.close()
    
    def summa_lines(pred_line, line, n):
        new_line = pred_line[:n]
        elems = [int(a)+int(b) for a,b in zip(pred_line[n:], line[n:])]
        return new_line + elems
    
    #Формируем список со суммой значений сгруппированой по комбинации строк
    new_lines = []
    for k, line in enumerate(lines):
        elems = line.replace('\n','').split('\t')
        if k == 0:
            pred_elems = elems
        if pred_elems[:n] == elems[:n]:
            if k == 0:
                new_lines.append(elems)
                continue
            new_lines[-1] = summa_lines(pred_elems, elems, n)  
        else:
            new_lines.append(elems)
        pred_elems = elems
        
    #Запись сформированного списка в файл
    file = open(result_group_filename,'w')
    writer = csv.writer(file, delimiter='\t')
    writer.writerow(head)
    for line in new_lines:
        writer.writerow(line)
    file.close()