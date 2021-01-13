This is a simple program (still in alpha) for making spectra analysis
from germanium detectors.

The program accepts 3 different file formats, ("mca" the pocket
version, "Txt" gamma view format, "SPE" ("spe") Boulby ("Snolab") format.)

IT'S NECESSARY PYTHON>=3.6, pip3 and git.


For installing (in Debian base systems with apt like Ubuntu), simply do:

	1. Run:

			sudo python3 install_sudo.py
	
	2. Or as 'su', run:

			apt upgrade python3-pip && pip3 install -r requirements.txt

	   and run out of root:
		
			python3 install_su.py

You can also install in manually using the instructions given at the tutorial, see the last
link given within this file.

For updating, simply do:

	1. Run:

			python3 update.py

	2. Or run, within the directory of the repository:

			git pull

	   and run as 'su':
		
			pip3 install -r requirements.txt

Download the database from this link:

https://bit.ly/2VOzuO1

Save it under the "Path/to/histoGe/myDatabase/" folder.

Open a new terminal and you should be
able to do a:

$ histoGe
usage: histoGe file.extension [-c data4fits.info]
Valid extensions are:
		SPE (spe)
		mca
		Txt

You should be able to see a similar output.

I'll edit this document later to show a couple of examples. Remember
this is still alpha!!

You can find the tutorial in the following link

https://docs.google.com/document/d/1uJFUylDsRrZgDNq3LurjP1XlhqiJvKm606XkQqTPGvI/edit?usp=sharing

Use the following for citing the code:

[![DOI](https://zenodo.org/badge/294481746.svg)](https://zenodo.org/badge/latestdoi/294481746)