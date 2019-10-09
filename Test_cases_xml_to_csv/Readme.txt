Test cases list script

The purpose of this script is to allow you to convert an xml exported from TestLink into a csv file. 
This is specific to exporting xml files from the Test Specification section, but it could be extended to the Requirement Specification section as well.

The file imported contains all the details to create new test cases items in the Test specification section of TestLink. 

The flow is the following:
* Add the xml file(s) exported from TestLink to the same folder than the script
* From a terminal window, pass as a parameter the name of the xml file and launch the script

One output file is created per script launch. It contains as many columns as test suite listed in the xml file, 
as well as the following details for each test case:
- Path (one column per parent Test Suite)
- ID
- Summary
- Number of steps


The script is written in Python version 3.
