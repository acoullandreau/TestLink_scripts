from xml.etree.ElementTree import ElementTree
import sys
import pathlib

config = {
	'columns': [
		'Test Case ID',
		'Number of Steps',
		'Test Summary'
	]
}

def processTree(tree):
	output = ''
	root = tree.getroot()
	max_depth = findDepth(root)

	output_filename = pathlib.Path(sys.argv[1]).stem + '.csv'
	f = open(output_filename, "w", encoding="utf-8")

	writeHeader(f, max_depth)

	processTestSuite(root, f, [], max_depth)

def findDepth(testsuite, depth = 1):
	testsuites = testsuite.findall('testsuite')
	max_depth = depth
	for entry in testsuites:
			curr_depth = findDepth(entry, depth + 1)
			if curr_depth > max_depth:
				max_depth = curr_depth
	return max_depth

def processTestSuite(testsuite, file, parents, max_depth):
	testsuites = testsuite.findall('testsuite')

	parents_copy = parents.copy()
	parents_copy.append(testsuite.attrib['name']);

	if len(testsuites) == 0:
		processLine(testsuite, file, parents_copy, max_depth)
	else:
		for entry in testsuites:
			processTestSuite(entry, file, parents_copy, max_depth)

def processLine(testsuite, file, parents, max_depth):
	testcases = testsuite.findall('testcase')
	for entry in testcases:
		for i in range(0, max_depth):
			if i < len(parents):
				file.write(parents[i]+';')
			else:
				file.write(';')
		file.write(findExternalId(entry)+';');
		file.write(calcNumberOfSteps(entry)+';');
		file.write(entry.attrib['name']+';');
		file.write('\n')


def findExternalId(testcase):
	externalId = testcase.find('externalid')
	return externalId.text

def calcNumberOfSteps(testcase):
	return str(len(list(testcase.iter('step_number'))))

def writeHeader(file, max_depth):
	for i in range(0, max_depth):
		file.write('Test Suite Level '+str(i+1)+';');
	for entry in config['columns']:
		file.write(entry+';')
	file.write('\n')

if len(sys.argv) == 2:
	file = sys.argv[1]
	tree = ElementTree()
	tree.parse(file)

	processTree(tree)
else:
	print('Please specify the file to parse.')


