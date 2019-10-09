import re
from xml.sax.saxutils import escape


class Req_spec:

    def __init__(self,doc_id):
        self.doc_id = doc_id
        self.title = ''
        self.subcat_dict = {}
        self.req_dict = {}


    #method get Req_spec --> return an existing instance of the Req_spec or creates it in the dictionary
    def get_Req_spec(self,doc_id):
        if doc_id not in self.subcat_dict:
            self.subcat_dict[doc_id] = Req_spec(doc_id)
        return self.subcat_dict[doc_id]

    #method get Requirement --> return an existing instance of the Requirement or creates it in the dictionary
    def get_Requirement(self,doc_id):
        if doc_id not in self.req_dict:
            self.req_dict[doc_id]=Requirement(doc_id)
        return self.req_dict[doc_id]

    #methods print xml --> build the xml file from the instances of the objects created
    #the method calls itself as there can be TestSuite parents of other TestSuites; as we "get" an instance of a test suite, we also get the dictionary associated
    #we can then loop through each key of that dictionary, until we get to the testcases dictionary
    #after going through all entries, we append the xml tags in the end
    def print_xml(self):
        body = '<req_spec title="{0}"  doc_id="{1}"> <type>1</type>'.format(self.title,self.doc_id)
        for entry in self.subcat_dict:
            req_spec = self.subcat_dict[entry]
            body+=req_spec.print_xml()
        for entry in self.req_dict:
            req = self.req_dict[entry]
            body+='<requirement><docid>{0}</docid><title>{1}</title><description>{2}</description><status>V</status><type>2</type><expected_coverage>1</expected_coverage></requirement>'.format(req.doc_id,req.title, req.description)
        body+='</req_spec>'
        return body


#xml structure
        #<req_spec title={0}  doc_id={1}>
            #<type><1></type>
        #</req_spec>



class Requirement:
    
    def __init__(self,doc_id):
        self.doc_id = doc_id
        self.title = ''
        self.description = ''


    #xml structure
        #<requirement>
            #<docid><{0}></docid>
            #<title><{1}></title>
            #<description><{2></description>
            #<status><V></status>
            #<type><2></type>
        #</requirement>




#File format
#Colonne A: Doc_ID Req_spec
#Colonne B: Title Req_spec
#Colonne C: Subcat name
#Colonne D: Doc_ID Requirement
#Colonne E: Title Requirement
#Colonne F: Description Requirement


#It is essential to use "self" in the methods
#when calling a method one should always refer to which instance is considered (can be self)


