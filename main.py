import csv, json, sys
import argparse
from parser import get_n, get_columns_names, preprocessing_csv_one, preprocessing_csv_two
from parser import preprocessing_json_file, preprocessing_xml_file, sort_resulting_file, group_result_file
# from parser import get_n, get_columns_names


def preprocessing_files(file_name_one,
                        file_name_two,
                        file_name_json,
                        file_name_xml,
                        file_name_result):

    file_one = open(file_name_one,'r')
    reader = csv.DictReader(file_one)
    n = get_n(reader)
    fields = get_columns_names(reader)

    out_f = open('test_out.csv','w')
    writer = csv.DictWriter(out_f, fieldnames=fields, delimiter=',')
    writer.writeheader()

    preprocessing_csv_one(reader, n, fields, writer)
    file_one.close()

    try:
        file_two = open(file_name_two,'r')
        reader = csv.DictReader(file_two)
        preprocessing_csv_two(reader, n, fields, writer)
        file_two.close()
    except Exception as exc:
        print('Failed to process the {} file, error: {}'.format(file_name_two, exc))
        out_f.close()
        return

    try:
        file_json = open(file_name_json,'r')
        data = json.load(file_json)
        file_json.close()
        preprocessing_json_file(data, fields, writer)
    except Exception as exc:
        print('Failed to process the {} file, error: {}'.format(file_name_json, exc))
        out_f.close()
        return
    try:
        preprocessing_xml_file(file_name_xml, fields, writer)
    except Exception as exc:
        print('Failed to process the {} file, error: {}'.format(file_name_xml, exc))
        out_f.close()
        return
    out_f.close()

    try:
        sort_resulting_file('test_out.csv', file_name_result)
    except Exception as exc:
        print('Failed to sort result file, error: {}'.format(exc))


    group_result_file(file_name_result,'adv_results.tsv', n)


preprocessing_files('csv_data_1.csv','csv_data_2.csv', 'json_data.json', 'xml_data.xml', 'result_test.tsv')
