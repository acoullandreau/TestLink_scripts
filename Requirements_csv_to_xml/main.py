import re
import csv
from classfile import Req_spec

root_dict = {}

# function to check if a category is in the dictionary of categories
def check_cat(cat_id):
    if cat_id not in root_dict:
        root_dict[cat_id] = Req_spec(cat_id)
    return root_dict[cat_id]


# file name FeaturesList.csv, separators ;
# creates an aray per row
with open('FeaturesList.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    # for each cell of each line, creation classes instances of the TestSuites, TestCases and Steps using the methods of the classes
    row_id = 1
    for row in readCSV:
        #row_id is used to avoid parsing the first line (header in the file)
        if row_id == 1:
            row_id += 1
            continue
        cat_id = row[0]
        category = check_cat(cat_id)
        category.title = row[1]
        subcat_id = row[2]
        subcat_name = row[3]
        # calls the get_TestSuite method for the Test Suite category
        subcategory = category.get_Req_spec(subcat_id)
        subcategory.title = subcat_name
        feat_id = row[4]
        feat_tit = row[5]
        feat_des = row[6]
        feature = subcategory.get_Requirement(feat_id)
        feature.title = feat_tit
        feature.description = feat_des
        row_id += 1


#generates the xml
    for entry in root_dict:
        xml_file = root_dict[entry].print_xml()
        f= open(entry+".txt","w+")
        f.write('<?xml version="1.0" encoding="UTF-8"?>')
        f.write('<requirement-specification>')
        f.write(xml_file)
        f.write('</requirement-specification>')



