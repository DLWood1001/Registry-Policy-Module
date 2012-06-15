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

    def __str__(self):
        return str(self.header) + str(self.body)
    

class RPHeader(object):
    def __init__(self):
        """Initialization method
        
        Just adds the signature and version property of the Registry.pol file.
        
        When used with the reader, these values will be over written.
        When used with the writer, these values can be used as defaults.
        """
        self.signature  = RP_SIGNATURE
        self.version    = RP_VERSION
    
    def __str__(self):
        return struct.pack('<II', self.signature, self.version)
    

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
    
    def __str__(self):
        body = ''
        
        for policy in self.policies:
            body += str(policy)
        
        return body 
    

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
    
    def __str__(self):
        policy = POLICY_ENTER_DELIM
        policy += self.key + POLICY_SECTION_TERM
        policy += POLICY_SECTION_DELIM
        policy += self.value + POLICY_SECTION_TERM
        policy += POLICY_SECTION_DELIM
        policy += struct.pack('<I', self.regtype)
        policy += POLICY_SECTION_DELIM
        policy += struct.pack('<I', self.size)
        
        if self.regtype == 1:
            policy += self.data + POLICY_SECTION_TERM
        elif self.regtype == 4:
            policy += struct.pack('<I', self.data)
        
        policy += POLICY_EXIT_DELIM
        
        return policy
    
    
