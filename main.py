
import csv, json

from parser import get_n, get_columns_names, preprocessing_csv_one, preprocessing_csv_two, preprocessing_json_file, preprocessing_xml_file
# from parser import get_n, get_columns_names

file = open('csv_data_1.csv','r')
reader = csv.DictReader(file)
n = get_n(reader)
fields = get_columns_names(reader)


out_f = open('test_out.csv','w')
writer = csv.DictWriter(out_f, fieldnames=fields, delimiter=',')
writer.writeheader()

file = open('csv_data_1.csv','r')
reader = csv.DictReader(file)
preprocessing_csv_one(reader, n, fields, writer)
file.close()

file = open('csv_data_2.csv','r')
reader = csv.DictReader(file)
preprocessing_csv_two(reader, n, fields, writer)
file.close()

file = open('json_data.json','r')
data = json.load(file)
file.close()

preprocessing_json_file(data, fields, writer)
preprocessing_xml_file('xml_data.xml', fields, writer)

out_f.close()