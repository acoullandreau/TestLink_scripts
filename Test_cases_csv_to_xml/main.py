import re
import csv
from classfile import TestSuite

root_dict = {}

# function to check if a category is in the dictionary of categories
def check_cat(cat_name):
    if cat_name not in root_dict:
        root_dict[cat_name] = TestSuite(cat_name)
    return root_dict[cat_name]


# file name TestPlanB4.csv, separators ;
# creates an aray per row
with open('TestPlanB4.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    # for each cell of each line, creation classes instances of the TestSuites, TestCases and Steps using the methods of the classes
    row_id = 1
    for row in readCSV:
        #row_id is used to avoid parsing the first line (header in the file)
        if row_id == 1:
            row_id += 1
            continue
        cat_name = row[0]
        category = check_cat(cat_name)
        subcat_name = row[1]
        # calls the get_TestSuite method for the Test Suite category
        subcategory = category.get_TestSuite(subcat_name)
        subcategory.detail = row[2]
        ent_name = row[3]
        entity = subcategory.get_TestSuite(ent_name)
        case_name = row[4]
        case_sum = row[5]
        case_precon = row[6]
        case = entity.get_TestCase(case_name)
        #the TestCase case is created from the entity Test Suite, and other attributes are assigned after its creation (just self and name as mandatory attributes)
        case.summary=case_sum
        case.preconditions=case_precon
        case_descr = row[7]
        case_acc = row[8]
        case.add_step(case_descr, case_acc, row_id)
        row_id += 1


#generates the xml
    for entry in root_dict:
        xml_file = root_dict[entry].print_xml()
        f= open(entry+".txt","w+")
        f.write('<?xml version="1.0" encoding="UTF-8"?>')
        f.write(xml_file)




