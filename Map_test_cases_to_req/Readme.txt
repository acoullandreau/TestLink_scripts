Test mapping script

The purpose of this script is to allow you to create an xml file (.txt) that can be imported to TestLink.
The file imported will manage the association of a test case with on or more requirements. 

The flow is the following:
* Add a csv file built with the same structure than the example in the same folder than the script
* From a terminal window, launch the script
* Import in TestLink, in the Test Specification section the files. The import should be performed from the highest level of Test Suite possible.

One output file is created per category identified in the first column, supposed to be the highest level of Test Suite you want to consider.

The script is written in Python version 3.