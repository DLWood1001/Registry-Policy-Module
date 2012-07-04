import struct

RP_SIGNATURE    = 0x67655250
RP_VERSION      = 0x00000001

POLICY_ENTER_DELIM      = u'['.encode('utf_16_le')
POLICY_EXIT_DELIM       = u']'.encode('utf_16_le')
POLICY_SECTION_DELIM    = u';'.encode('utf_16_le')
POLICY_SECTION_TERM     = u'\0'.encode('utf_16_le')

class RPData(object):
    def __init__(self):
        """Initialization method
        
        Just adds two object propertises
        
        """
        self.header	= RPHeader()
        self.body	= RPBody()

    def __to_str(self):
        return self.header + self.body
    
    def __str__(self):
        return self.__to_str()
    
    def __add__(self, right):
        return self.__to_str() + right
    
    def __radd__(self, left):
        return left + self.__to_str()
    

class RPHeader(object):
    def __init__(self):
        """Initialization method
        
        Just adds the signature and version property of the Registry.pol file.
        
        When used with the reader, these values will be over written.
        When used with the writer, these values can be used as defaults.
        """
        self.signature  = RP_SIGNATURE
        self.version    = RP_VERSION
    
    def __to_str(self):
        return struct.pack('<II', self.signature, self.version)
    
    def __str__(self):
        return self.__to_str()
    
    def __add__(self, right):
        return self.__to_str() + right
    
    def __radd__(self, left):
        return left + self.__to_str()
        

class RPBody(object):
    def __init__(self):
        """Initialization method
        
        Just adds a dictionary to contain the various policies contained inside the Registry.pol file.
        """
        self.policies   = []

    def add_policy(self, policy):
        """Adds a single policy to the rp data object.
        
        I know this is not so Pythonic, but I like the look of the setter method in the code implementing the changes.
        
        Note: No error checking is done.
        """
        self.policies.append(policy)
    
    def add_policies(self, policies):
        """Adds a multiple policies to the rp data object.
        
        I know this is not so Pythonic, but I like the look of the setter method in the code implementing the changes.
        
        Note: No error checking is done.
        """
        self.policies += policies
    
    def __to_str(self):
        body = ''
        
        for policy in self.policies:
            body += policy
        
        return body
    
    def __str__(self):
        return self.__to_str()
    
    def __add__(self, right):
        return self.__to_str() + right
    
    def __radd__(self, left):
        return left + self.__to_str()
    

class RPPolicy(object):
    def __init__(self):
        """Initialization method
        
        Sets instance properties.  I've added some initialization to the data types although it is probably not needed.
        """
        
        self.key        = unicode('utf_16_le')
        self.value      = unicode('utf_16_le')
        self.regtype    = int()
        self.size       = int()
        self.data       = None
    
    def __to_str(self):
        policy = POLICY_ENTER_DELIM
        policy += self.key + POLICY_SECTION_TERM
        policy += POLICY_SECTION_DELIM
        policy += self.value + POLICY_SECTION_TERM
        policy += POLICY_SECTION_DELIM
        policy += struct.pack('<I', self.regtype)
        policy += POLICY_SECTION_DELIM
        policy += struct.pack('<I', self.size)
        policy += POLICY_SECTION_DELIM
        
        if self.regtype == 0: pass
        elif self.regtype == 1: policy += self.data + POLICY_SECTION_TERM
        elif self.regtype == 4: policy += struct.pack('<I', self.data)
        else: raise NotImplementedError()
        
        policy += POLICY_EXIT_DELIM
        
        return policy
    
    def __str__(self):
        return self.__to_str()
    
    def __add__(self, right):
        return self.__to_str() + right
    
    def __radd__(self, left):
        return left + self.__to_str()        
    
    
