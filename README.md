README.TXT
==========

rp is python module used to parse Registry.pol files. The Registry.pol is the location where Microsoft stores the settings created through Authentication Templates. This is only useful for the sys admins out there.

## Basic Usage
Simple Python script example:

	RPData = rp.RPData()
	RPReader = rp.reader('Registry.pol', RPData)

	for policy in RPData.body.policies:
		# Do your stuff here
		# Check the 'data' sub module under 'rp' to understand the policy data structure.
		pass
