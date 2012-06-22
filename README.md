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

## ToDo
* Refactor the name of the 'RPData' class.
* Refactor the names of the reader > states.py classes.
* Handle advanced 'values' fields
* Build 'util' or 'tools' classes
	* Remove duplicates
	* Convert to companion .reg

## Registry.pol File Format
The Registry.pol file is a relatively simple file.  It contains a simple header and a body containing multiple registry policies (entries).

### Header
Signature = 0x67655250 (4 bytes; Unsigned Int)  
Version = 0x00000001 (4 bytes; Unsigned Int)  

### Body
The body contains multiple entries in the following structure:  
	[Key;Value;Type;Size;Data]


* **Key**: Null terminated byte array encoded in UTF-16LE.  
* **Value**: Null terminated byte array encoded in UTF-16LE. It is possible for the value to contain a special command in addition or replacement for a typical registry value.
	* **\*\*DeleteValues**: A semicolon-delimited list of values to delete. Use as a value of the associated key.
	* **\*\*Del.valuename**: Deletes a single value. Use as a value of the associated key.
	* **\*\*DelVals**: Deletes all values in a key. Use as a value of the associated key.
	* **\*\*DeleteKeys**: A semicolon-delimited list of keys to delete.
	* **\*\*SecureKey**: **SecureKey=1 secures the key, giving administrators and the system full control, and giving users read-only access. **SecureKey=0 resets access to the key to whatever is set on the root.
	
* **Type**: 4 bytes; Unsigned Int. Directly corrisponds to the windows registry data types.
	* **REG_NONE (0)**: No type
	* **REG_SZ (1)**: String type (ASCII)
	* **REG_EXPAND_SZ (2)**: String, includes %ENVVAR% (expanded by caller) (ASCII)
	* **REG_BINARY (3)**: Binary format, callerspecific
	* **REG_DWORD (4)**: DWORD in little endian format
	* **REG_DWORD_LITTLE_ENDIAN (4)**: DWORD in little endian format
	* **REG_DWORD_BIG_ENDIAN (5)**: DWORD in big endian format
	* **REG_LINK (6)**: Symbolic link (UNICODE)
	* **REG_MULTI_SZ (7)**: Multiple strings, delimited by \0, terminated by \0\0 (ASCII)
	* **REG_RESOURCE_LIST (8)**: Resource list? huh?
	* **REG_FULL_RESOURCE_DESCRIPTOR (9)**: Full resource descriptor? huh?
	* **REG_RESOURCE_REQUIREMENTS_LIST (10)**:
	* **REG_QWORD (11)**: QWORD in little endian format
	* **REG_QWORD_LITTLE_ENDIAN (11)**: QWORD in little endian format

* **Size**: 4 bytes; Unsigned Int.  
* **Data**: Depending on the 'Type' field. Note: REG_SZ is encoded in UTF-16LE and null terminated.  




