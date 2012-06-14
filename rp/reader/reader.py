import sys

from rp import parser
import states

class Reader(object):
    """
    The Reader class is used to parse Registry.pol files into RPData objects.
    """
    
    def __init__(self, input_file=None, registry_pol=None):
        """
        This method creates the Registry.pol file parser.  The parser is another sub-module of the rp class.
        The states of the parser can be found in the states.py file which is part of the reader module.
        
        @param input_file: Contains a valid path/to/Registry.pol string.
        @param registry_pol: Contains a valid RPData object.
        """
        self.RPParser = parser.Parser()
        
        self.RPParser.add_states(signature=states.Signature, version=states.Version)
        self.RPParser.add_states(policy_enter=states.PolicyEnter, policy_delim=states.PolicyDelim, policy_exit=states.PolicyExit)
        self.RPParser.add_states(policy_key=states.PolicyKey, policy_value=states.PolicyValue, policy_reg_type=states.PolicyRegType, policy_size=states.PolicySize, policy_data=states.PolicyData)
        
        if (input_file and (registry_pol != None)):
            self.input_file(input_file)
            self.read(registry_pol)
    
    def input_file(self, input_file):
        """
        Method to change the input file of the Reader class.
        
        @param input_file: Contains a valid path/to/Registry.pol string.
        """
        self.input_file = input_file
    
    def read(self, registry_pol):
        """
        Method to read the Registry.pol file
        
        @param registry_pol: Contains a valid RPData object.
        """
        memory = dict()
        memory['rpdata'] = registry_pol
        
        self.RPParser.parse(self.input_file, 'signature', memory)
    




