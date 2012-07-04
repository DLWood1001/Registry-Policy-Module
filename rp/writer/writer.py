from rp.data import data
import struct


# Writer class
class Writer(object):
    """
    This class is used to build a registry.pol file off of a RPData object.
    
    Currently the RPWriter works.. but could be structured better.
    """
    
    def __init__(self, output_file=None, registry_pol=None):
        self.output_file = None
        
        if (output_file and (registry_pol != None)):
            self.output_file(output_file)
            self.write(registry_pol)
    
    
    def write(self, registry_pol=None):
        
        header = data.RPHeader()
        
        file_handle = open(self.output_file, 'wb')
        
        # Write file header
        file_handle.write(str(registry_pol))
    
