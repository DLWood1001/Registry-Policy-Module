RP_SIGNATURE    = 0x67655250
RP_VERSION      = 0x00000001


class RPData(object):
	def __init__(self):
        """Initialization method
        
        Just adds two object propertises
        """
		self.header	= RPHeader()
		self.body	= RPBody()
    

class RPHeader(object):
    def __init__(self):
        """Initialization method
        
        Just adds the signature and version property of the Registry.pol file.
        
        When used with the reader, these values will be over written.
        When used with the writer, these values can be used as defaults.
        """
        self.signature  = RP_SIGNATURE
        self.version    = RP_VERSION
    

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
    
