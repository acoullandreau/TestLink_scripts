import re
from xml.sax.saxutils import escape



class Test_category:

    def __init__(self,name):
        self.name = name
        self.case_dict = {}


    #method get Test_Case --> return an existing instance of the Test_Case or creates it in the dictionary
    def get_Test_Case(self,ext_id):
        if ext_id not in self.case_dict:
            self.case_dict[ext_id] = Test_Case(ext_id)
        return self.case_dict[ext_id]



    #methods print xml --> build the xml file from the instances of the objects created
    #the method calls itself as there can be TestSuite parents of other TestSuites; as we "get" an instance of a test suite, we also get the dictionary associated
    #we can then loop through each key of that dictionary, until we get to the testcases dictionary
    #after going through all entries, we append the xml tags in the end
    def print_xml(self):
        body = '<testcases>'
        for entry in self.case_dict:
            case = self.case_dict[entry]
            body+='<testcase name="{0}"><externalid>{1}</externalid><requirements>'.format(case.name,case.ext_id)
            for entry in case.req_spec_dict:
                req_spec = case.req_spec_dict[entry]
                body+='<requirement><req_spec_title>{0}</req_spec_title>'.format(req_spec.title)
                for entry in req_spec.req_dict:
                    req = req_spec.req_dict[entry]
                    body+='<docid>{0}</docid><title>{1}</title>'.format(req.doc_id,req.title)
                body+='</requirement></requirements></testcase>'
        body+='</testcases>'
        return body



class Test_Case:

    def __init__(self,ext_id):
        self.ext_id = ext_id
        self.name = ''
        self.req_spec_dict = {}


    #method get Req_spec --> return an existing instance of the Req_spec or creates it in the dictionary
    def get_Req_spec(self,title):
        if title not in self.req_spec_dict:
            self.req_spec_dict[title] = Req_spec(title)
        return self.req_spec_dict[title]




class Requirement:
    
    def __init__(self,doc_id):
        self.doc_id = doc_id
        self.title = ''



class Req_spec:

    def __init__(self,title):
        self.title = title
        self.req_dict = {}

    #method get Requirement --> return an existing instance of the Requirement or creates it in the dictionary
    def get_Requirement(self,title):
        if title not in self.req_dict:
            self.req_dict[title]=Requirement(title)
        return self.req_dict[title]





#xml structure
    #<testcases>
        #<testcase name={}>
           #<externalid>{}</externalid>
            #<requirements>
                #<requirement>
                    #<req_spec_title>{}</req_spec_title>
                    #<doc_id>{}</doc_id>
                    #<title>{}</title>
                #</requirement>
            #</requirements>
        #</testcase>
    #</testcases>




#File format
#Colonne A: External ID test case
#Colonne B: Name test case
#Colonne C: Title Requirement_Specification
#Colonne D: Doc_ID Requirement
#Colonne E: Title Requirement


#It is essential to use "self" in the methods
#when calling a method one should always refer to which instance is considered (can be self)


