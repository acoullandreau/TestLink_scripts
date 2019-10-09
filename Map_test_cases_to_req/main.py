#https://github.com/MrBricodage/TestLink--ExcelMacros

import re
import csv
from classfile import Test_category

root_dict = {}

# function to check if a category is in the dictionary of categories
def check_cat(cat_id):
    if cat_id not in root_dict:
        root_dict[cat_id] = Test_category(cat_id)
    return root_dict[cat_id]


# file name FeaturesList.csv, separators ;
# creates an aray per row
with open('Map_req_case.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    # for each cell of each line, creation classes instances of the TestSuites, TestCases and Steps using the methods of the classes
    row_id = 1
    for row in readCSV:
        #row_id is used to avoid parsing the first line (header in the file)
        if row_id == 1:
            row_id += 1
            continue
        cat_name = row[0]
        test_category = check_cat(cat_name)
        ext_id = row[1]
        test_case = test_category.get_Test_Case(ext_id)
        test_case.name = row[2]
        req_spec_name = row[3]
        # calls the get_TestSuite method for the Test Suite category
        req_spec = test_case.get_Req_spec(req_spec_name)
        req_id = row[4]
        req_tit = row[5]
        requirement = req_spec.get_Requirement(req_id)
        requirement.title = req_tit
        row_id += 1


#generates the xml
    for entry in root_dict:
        xml_file = root_dict[entry].print_xml()
        f= open(entry+".txt","w+")
        f.write('<?xml version="1.0" encoding="UTF-8"?>')
        f.write(xml_file)



