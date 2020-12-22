import os
import subprocess

try:
	os.system('apt upgrade python3-pip')
	os.system('pip3 install -r .requirements/requirements.txt')
	path = subprocess.getoutput("pwd")+"/histoGe.py"
	os.system("mkdir -p ~/.myPrograms")
	a = "cd ~/.myPrograms && ln -s "+ path + "   histoGe"
	os.system(a)
	if (len(subprocess.getoutput("grep 'export PATH=$PATH:~/.myPrograms' ~/.bashrc")))==0:
		os.system("echo 'export PATH=$PATH:~/.myPrograms' >> ~/.bashrc")
except:
	print('ERROR: Failed to install. Please, install manually.')
