import sys

from rp import parser
import states

class Reader(object):
    def __init__(self, input_file=None, registry_pol=None):
        self.RPParser = parser.Parser()
        
        self.RPParser.add_states(signature=states.Signature, version=states.Version)
        self.RPParser.add_states(policy_enter=states.PolicyEnter, policy_delim=states.PolicyDelim, policy_exit=states.PolicyExit)
        self.RPParser.add_states(policy_key=states.PolicyKey, policy_value=states.PolicyValue, policy_reg_type=states.PolicyRegType, policy_size=states.PolicySize, policy_data=states.PolicyData)
        
        if (input_file and (registry_pol != None)):
            self.input_file(input_file)
            self.read(registry_pol)
    
    def input_file(self, input_file):
        self.input_file = input_file
    
    def read(self, registry_pol):
        memory = dict()
        memory['rpdata'] = registry_pol
        
        self.RPParser.parse(self.input_file, 'signature', memory)
    




