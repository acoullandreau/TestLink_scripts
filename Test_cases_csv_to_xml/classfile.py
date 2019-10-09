import re
from xml.sax.saxutils import escape

class TestSuite:

    def __init__(self,name):
        self.name = name
        self.detail = ''
        self.suite_dict = {}
        self.case_dict = {}

    #method get TestSuite --> return an existing instance of the TestSuite or creates it in the dictionary
    def get_TestSuite(self, name):
        if name not in self.suite_dict:
            self.suite_dict[name] = TestSuite(name)
        return self.suite_dict[name]

    #method get TestCase --> return an existing instance of the TestCase or creates it in the dictionary
    def get_TestCase(self,name):
        if name not in self.case_dict:
            self.case_dict[name]=TestCase(name)
        return self.case_dict[name]

    #methods print xml --> build the xml file from the instances of the objects created
    #the method calls itself as there can be TestSuite parents of other TestSuites; as we "get" an instance of a test suite, we also get the dictionary associated
    #we can then loop through each key of that dictionary, until we get to the testcases dictionary
    #after going through all entries, we append the xml tags in the end
    def print_xml(self):
        body = '<testsuite name="{0}"><details>{1}</details>'.format(self.name,self.detail)
        for entry in self.suite_dict:
            suite = self.suite_dict[entry]
            body+=suite.print_xml()
        for entry in self.case_dict:
            case = self.case_dict[entry]
            body+=case.print_xml()
        body+='</testsuite>'
        return body

    #xml structure
        #<testsuite name = {0}>
            #<details>{1}</details>
        #</testsuite>


class TestCase:

    def __init__(self,name):
        self.name = name
        self.summary = ''
        self.preconditions = ''
        self.steps =[]

    #method add step --> adds each step to the array
    def add_step(self, cell1, cell2, row_id):
        self.steps = Step.parse_steps(cell1, cell2, row_id)


    #methods print xml --> build the xml file from the instances of the objects created
    def print_xml(self):
        body = '<testcase name="{0}"><summary>{1}</summary><preconditions>{2}</preconditions><steps>'.format(self.name,self.summary, self.preconditions)
        for elem in self.steps:
            body+=elem.print_xml()
        body+='</steps></testcase>'
        return body


    #xml structure
        #<testcase name = {2}>
            #<summary>{3}</summary>
            #<preconditions>{4}</preconditions>
        #</testcase>


class Step:

    def __init__(self, number, action):
        self.number = number
        self.action = action
        self.expected_result = ''

    #method parse steps --> gets the content of a cell and divides it into as many elements as there are lines/numbers in the cell

    #method parse_list breaks cells and creates an array of sets for its content
    #if a cell contains several lines, the array will contain several sets
    #each set is an array of the content of each line, separating the number at the beginning of the line (step number) from the text after (action)
    def parse_list(cell, complete_numbers, row_id):
        number = 0
        content = ''

        p_sub = re.compile(r'\d+\.\d+')
        p_item = re.compile(r'(\d+)\.\s?(.*)')
                #compile the regex used to separate the content in a cell (either just a number (1.) or a subcategory (1.1))
        #we want the subcategories to be inside an action: 
        #1.1 goes into 1., we do not want to create a new step 1 with the beginning of 1.1, but we want to append it to the 1. content

        broken_cell = cell.split('\n')
        #creates an array with each line of a cell
        result = []
        
        started = False
        #this marker indicates if we already have started filling the content variable (str)
        item_count = 1
        #this counter memorizes the number of the step we are currently in, in case of a line without number
        
        for line in broken_cell:
            line = escape(line)
        #we loop through the array of lines
            if line != '':
            #we ignore empty lines
                is_sub = p_sub.match(line)
                
                if is_sub == None:
                #if it is a line without subcategory (i.e 1, and not 1.1)
                                        
                    item = p_item.findall(line)
                    #item is an array built from the regex that separates number from action

                    if len(item) > 0:
                        if started == True:
                        #we found a new step in the line (we found 2.)
                        #but we already have content in content (from 1.)
                        #we empty content from 1. to be able to write for 2.
                            result.append([number, content])
                            item_count += 1
                            #we got to a step above (for example, we got to 2)
                            number = 0
                            content = ''
                            #we clear number and temporary content
                    #the regex succeeded (matched)
                    #we assign the number and the action to the content array
                    #started is True because content is not empty anymore
                        number = item[0][0]
                        content += item[0][1]
                        started = True

                    else:
                    #the regex didn't match (it's not a 1.sth, nor a sucategory)
                    #warning because the format is not as expected if we are in the case of a step (complete_number)
                    #complete_number parameter defines whether we use the item count to complete the number
                    #useful for acc criteria --> if no number, writes -1 (will be used to add the acc to the last step)
                    #for steps, goes to the current step number (item count)
                        if started == True :
                            #this case handles multiple lines in acc cell without any number
                            content += '\n'+line

                        if complete_numbers == True:
                            print(row_id, 'Warning - Malformatted line: ', line)
                            result.append([str(item_count), line])
                        else:
                            number = -1
                            content += line
                            started = True
                        #we increment item_count because we just added one item (for the next iteration)
                        #as we added a new item we clear the content
                #if we have a line with a subcategory (i.e 1.1 and not 1), we append its content to the content of the category (1) with a line break
                else:
                    content += '\n'+line
        #this makes sure that the last iteration gets inserted
        #if there is just 1 line, it gets inserted here
        #if there are 2 lines, the first line gets inserted before inside the loop
        if number != 0:
            result.append([number, content])
            item_count += 1
        return result

    def parse_steps(cell1, cell2, row_id):
        #builds an array of each line in the cell
        steps = []
        step_list = Step.parse_list(cell1, True, row_id)
        #complete_number is set to True because we want to catch a line without an number if it is a step
        #the program "creates" the number for a line malformatted using the item_count
        #this îs a static method - no use of self as it is not for the instance looked at

        last_step = None
        for step_data in step_list:
            step = Step(step_data[0], step_data[1])
            steps.append(step)
            last_step = step

        acc_list = Step.parse_list(cell2, False, row_id)
        #complete_number is set to False because we want to associate a line without number to the last step
        #the program sets the number to -1 that is used in the loop below to manage the association to the last step

        for acc_data in acc_list:
            if acc_data[0] == -1:
            #if an acc is without a number, we want to associate it to the last available step registered
                if last_step != None:
                #this means that the parser found a step
                    last_step.expected_result = acc_data[1]
                else:
                #the acceptance criteria is for the entire test case, and will not be added to the XML (no field in TestLink)
                    print(row_id, 'Warning - Acceptance criteria without a step')
            else:
            #the acc is associated to the step with the same number
                for step in steps:
                    if step.number == acc_data[0]:
                        step.expected_result = acc_data[1]
                        break

        return steps


    def print_xml(self):
        body = '<step><step_number>{0}</step_number><actions>{1}</actions></step><expectedresults>{2}</expectedresults>'.format(self.number, self.action, self.expected_result)
        return body


    #note: for now, expectedresult is set aside and ignored
    #xml structure
        #<steps>
            #<step>
                #<step_number>{5}</step_number>
                #<actions>{6}</actions>
                #<expectedresults>{7}</expectedresults>
             #</step>
        #</steps>


#It is essential to use "self" in the methods
#when calling a method one should always refer to which instance is considered (can be self)


