from rp.data import data
import struct

# A few constants used in the Registry.pol header
POLICY_ENTER_DELIM      = u'['.encode('utf_16_le')
POLICY_EXIT_DELIM       = u']'.encode('utf_16_le')
POLICY_SECTION_DELIM    = u';'.encode('utf_16_le')
POLICY_SECTION_TERM     = u'\0'.encode('utf_16_le')

# Writer class
class Writer(object):
    """
    This class is used to build a registry.pol file off of a RPData object.
    
    Currently the RPWriter works.. but could be structured better.
    """
    def __init__(self, output_file=None, registry_pol=None):
        if (output_file and (registry_pol != None)):
            self.output_file(output_file)
            self.write(registry_pol)
        
    
    def output_file(self, output_file):
        """
        Access to change the output file..
        
        I don't know why I created this method.. might as well just access the property directly.
        """
        self.output_file = output_file
    
    def write(self, registry_pol=None):
        
        header = rp_data.RPHeader()
        
        file_handle = open(self.output_file, 'w')
        
        # Write file header
        file_handle.write(struct.pack('<II', header.signature, header.version))
        
        for policy in registry_pol.body.policies:
            file_handle.write(POLICY_ENTER_DELIM)
            file_handle.write(policy.key + POLICY_SECTION_TERM)
            file_handle.write(POLICY_SECTION_DELIM)
            file_handle.write(policy.value + POLICY_SECTION_TERM)
            file_handle.write(POLICY_SECTION_DELIM)
            file_handle.write(struct.pack('<I', policy.regtype))
            file_handle.write(POLICY_SECTION_DELIM)
            file_handle.write(struct.pack('<I', policy.size))
            file_handle.write(POLICY_SECTION_DELIM)
            
            if policy.regtype == 1:
                file_handle.write(policy.data)
                file_handle.write(POLICY_SECTION_TERM)
            elif policy.regtype == 4:
                file_handle.write(struct.pack('<I', policy.data))
            
            file_handle.write(POLICY_EXIT_DELIM)
        
    