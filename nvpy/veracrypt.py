import os
import subprocess
from Tkinter import *
import tkSimpleDialog

class veracrypt:

    def getpwd(self):
	root = Tk()
	root.withdraw()
	try:
	    password = tkSimpleDialog.askstring("Password", "Please enter password for VeraCrypt:", show='*')

	except Exception as e:
	    print("Error getting password: %s" % e )

	root.destroy()
	root.mainloop()

	return password

    def createKeyfile(self, random_source, keyfile):
	try:
	    p = subprocess.Popen('veracrypt --create-keyfile %s --random-source=%s' % (keyfile, random_source), stdin=None,stdout=subprocess.PIPE, shell=True)
	    output = p.communicate()[0]
	    print(output)

	except Exception as e:
		print("Error: %s" % e)

    def createContainer(self, config):
	self.config = config
	self.vc_password = self.getpwd()
	if not config.key_file:
	    self.key_file = os.path.join('/tmp/', 'vc_nvpy.keyfile')
	    self.createKeyfile(config.random_source, self.key_file)
	else:
	    self.key_file = os.path.join(config.db_path, config.key_file)

	
	cmd = 'veracrypt -t -c --encryption=%s -k %s --filesystem=%s --hash=%s -p \'%s\' --random-source=%s --size=%d --volume-type=%s %s' % (config.encryption_type, self.key_file, config.filesystem_type, config.hash_type, self.vc_password, config.random_source, config.size, config.volume_type, config.container_path)

	#Pattern to match: The VeraCrypt volume has been successfully created.
	pattern = re.compile('sucessfull')
	p = subprocess.Popen(cmd, stdin=None,stdout=subprocess.PIPE, shell=True)
	output = p.communicate()[0]
	print(output)

    def mountContainer(self, config):
	self.config = config
	if not config.key_file:
	    self.key_file = os.path.join('/tmp/', 'vc_nvpy.keyfile')
	else:
	    self.key_file = os.path.join(config.db_path, config.key_file)

	self.vc_password = self.getpwd()

	cmd = 'veracrypt -t -k %s --protect-hidden=%s -p \'%s\' %s %s' % (self.key_file,  config.protect_hidden, self.vc_password, config.container_path, config.db_path)
	#Pattern to match: The VeraCrypt volume has been successfully created.
	pattern = re.compile('sucessfull')

	p = subprocess.Popen(cmd, stdin=None,stdout=subprocess.PIPE, shell=True)
	output = p.communicate()[0]
	print(output.split('\n'))
	#lines = output.split('\n')
	#for line in output.split('\n'):
	    #match for sucess
	    #lineMatch = re.search(pattern, line)

    def unmountContainer(self, config):
	print("in unmount")
	#os.popen("truecrypt -t -d " + escape(opts['path']))

