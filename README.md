README.md
=========

rp is python module used to parse Registry.pol files. The Registry.pol is the location where Microsoft stores the settings created through Authentication Templates. This is only useful for the sys admins out there.

## Basic Usage
Simple Python script example:

	RPData = rp.RPData()
	RPReader = rp.reader('Registry.pol', RPData)

	for policy in RPData.body.policies:
		# Do your stuff here
		# Check the 'data' sub module under 'rp' to understand the policy data structure.
		pass

## Registry.pol File Format
The Registry.pol file is a relatively simple file.  It contains a simple header and a body containing multiple registry policies (entries).

### Header
Signature = 0x67655250 (4 bytes; Unsigned Int)  
Version = 0x00000001 (4 bytes; Unsigned Int)  

### Body
The body contains multiple entries encoded UTF16LE in the following format:  
[Key;Value;Type;Size;Data]

Key = null terminated byte array. Note: Encoded in unicode.  
Value = null terminated byte array. Note: Encoded in unicode.   
Type = 4 bytes; Unsigned Int.  Corrisponds to the windows registry data types.  
Size = 4 bytes; Unsigned Int.  
Data = byte array, depending on the 'Type' field. Note: REG_SZ is encoded in unicode and null terminated.  



