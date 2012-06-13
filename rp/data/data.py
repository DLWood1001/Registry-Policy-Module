RP_SIGNATURE    = 0x67655250
RP_VERSION      = 0x00000001


class RPData(object):
	def __init__(self):
		self.header	= RPHeader()
		self.body	= RPBody()
    

class RPHeader(object):
    def __init__(self):
        self.signature  = RP_SIGNATURE
        self.version    = RP_VERSION
    

class RPBody(object):
    def __init__(self):
        self.policies   = []

    def add_policy(self, policy):
        self.policies.append(policy)
    
    def add_policies(self, policies):
        self.policies += policies
    

class RPPolicy(object):
    def __init__(self):
        self.key        = unicode('utf_16_le')
        self.value      = unicode('utf_16_le')
        self.regtype    = int()
        self.size       = int()
        self.data       = None
    
