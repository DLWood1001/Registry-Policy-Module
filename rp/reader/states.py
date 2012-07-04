import rp.data
from rp.parser import State
import struct

POLICY_ENTER_DELIM      = u'['.encode('utf_16_le')
POLICY_EXIT_DELIM       = u']'.encode('utf_16_le')
POLICY_SECTION_DELIM    = u';'.encode('utf_16_le')
POLICY_SECTION_TERM     = u'\0'.encode('utf_16_le')

class Signature(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 4
        self.next_state     = 'version'
    
    def process(self, data):
        signature, = struct.unpack('<I', data)
        
        if signature != 0x67655250:
            raise Exception('Invalid File: Header')
        
        self.memory['rpdata'].header.signature = signature
        
        return True
    
    
class Version(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 4
        self.next_state     = 'policy_enter'
    
    def process(self, data):
        version, = struct.unpack('<I', data)
        
        if version != 1:
            raise Exception('Invalid File: Version')
        
        self.memory['rpdata'].header.version = version
        
        return True
    

class PolicyEnter(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 2
        self.next_state     = 'policy_key'
    
    def process(self, data):
        if data != POLICY_ENTER_DELIM:
            raise Exception('Invalid or Corrupt File: PolicyEnter Delim Missing')
        
        self.memory['policy'] = rp.data.RPPolicy()
        
        return True
    

class PolicyDelim(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 2
        self.next_state     = None
    
    def process(self, data):
        
        if data != POLICY_SECTION_DELIM:
            raise Exception('Invalid or Corrupt File: BodyDelim Delim Missing')
        
        self.next_state = self.memory['next_state']
        
        return True
    

class PolicyExit(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 2
        self.next_state     = 'policy_enter'
    
    def process(self, data):
        if data != POLICY_EXIT_DELIM:
            raise Exception('Invalid or Corrupt File: PolicyExit Delim Missing')

        self.memory['rpdata'].body.add_policy(self.memory['policy'])
                
        return True
    


class PolicyKey(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 2
        self.next_state     = 'policy_delim'
        
        self.key = u''.encode('utf_16_le') 
        
        self.memory['next_state'] = 'policy_value'
    

    def process(self, data):

        if data != POLICY_SECTION_TERM:
            self.key += data
            
            return False
        
        self.memory['policy'].key = self.key
        
        return True
    


class PolicyValue(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 2
        self.next_state     = 'policy_delim'
        
        self.value = u''.encode('utf_16_le')
        
        self.memory['next_state'] = 'policy_reg_type'

    def process(self, data):

        if data != POLICY_SECTION_TERM:
            self.value += data
            
            return False
        
        self.memory['policy'].value = self.value
        
        return True
    

class PolicyRegType(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 4
        self.next_state     = 'policy_delim'
        
        self.memory['next_state'] = 'policy_size'

    def process(self, data):
        
        regtype, = struct.unpack('<I', data)
        
        self.memory['policy'].regtype = regtype
        
        return True
    

class PolicySize(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 4
        self.next_state     = 'policy_delim'
        
        self.memory['next_state'] = 'policy_data'

    def process(self, data):
        
        size, = struct.unpack('<I', data)
        
        self.memory['policy'].size = size
        
        return True
    

class PolicyData(object):    
    def __new__(class_object, memory):
                
        regtype = memory['policy'].regtype
        
        '''
            #define REG_NONE                0       /* no type */
            #define REG_SZ                  1       /* string type (ASCII) */
            #define REG_EXPAND_SZ           2       /* string, includes %ENVVAR% (expanded by caller) (ASCII) */
            #define REG_BINARY              3       /* binary format, callerspecific */
            #define REG_DWORD               4       /* DWORD in little endian format */
            #define REG_DWORD_LITTLE_ENDIAN 4       /* DWORD in little endian format */
            #define REG_DWORD_BIG_ENDIAN    5       /* DWORD in big endian format  */
            #define REG_LINK                6       /* symbolic link (UNICODE) */
            #define REG_MULTI_SZ            7       /* multiple strings, delimited by \0, terminated by \0\0 (ASCII) */
            #define REG_RESOURCE_LIST       8       /* resource list? huh? */
            #define REG_FULL_RESOURCE_DESCRIPTOR    9       /* full resource descriptor? huh? */
            #define REG_RESOURCE_REQUIREMENTS_LIST  10
            #define REG_QWORD               11      /* QWORD in little endian format */
            #define REG_QWORD_LITTLE_ENDIAN 11      /* QWORD in little endian format */
        '''
        
        if regtype == 0: policy_data_object = super(PolicyData, class_object).__new__(PolicyDataREG_NONE)
        elif regtype == 1: policy_data_object = super(PolicyData, class_object).__new__(PolicyDataREG_SZ)
        elif regtype == 2: raise NotImplementedError('Data type 2 is not implemented')
        elif regtype == 3: raise NotImplementedError('Data type 3 is not implemented')
        elif regtype == 4: policy_data_object = super(PolicyData, class_object).__new__(PolicyDataREG_DWORD)
        elif regtype == 5: raise NotImplementedError('Data type 5 is not implemented')
        elif regtype == 6: raise NotImplementedError('Data type 6 is not implemented')
        elif regtype == 7: raise NotImplementedError('Data type 7 is not implemented')
        elif regtype == 8: raise NotImplementedError('Data type 8 is not implemented')
        elif regtype == 9: raise NotImplementedError('Data type 9 is not implemented')
        elif regtype == 10: raise NotImplementedError('Data type 10 is not implemented')
        elif regtype == 11: raise NotImplementedError('Data type 11 is not implemented')
        else: raise NotImplementedError('Unknown Data type')
        
        policy_data_object.__init__(memory)
        
        return policy_data_object
    

class PolicyDataREG_NONE(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 0
        self.next_state     = 'policy_exit'
        
        self.reg_sz         = u''.encode('utf_16_le')
    
    def process(self, data):
        return True


class PolicyDataREG_SZ(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 2
        self.next_state     = 'policy_exit'
        
        self.reg_sz         = u''.encode('utf_16_le')
    
    def process(self, data):
        
        if data != POLICY_SECTION_TERM:
            self.reg_sz += data
            
            return False
        
        self.memory['policy'].data = self.reg_sz
        
        return True
    

class PolicyDataREG_DWORD(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 4
        self.next_state     = 'policy_exit'
    
    def process(self, data):
        reg_dword, = struct.unpack('<I', data)
        
        self.memory['policy'].data = reg_dword
        
        return True
    
