# GINZENC3
python3 port of sabyenc (tested with python 3.7)


Copyright (C) 2003, 2011 Alessandro Duca <alessandro.duca@gmail.com>
Modified in 2016 by Safihre <safihre@sabnzbd.org> for use within SABnzbd
Modified in 2019 by dermatty <stephan@untergrabner.at> for use with python 3.7 and ginzibix
	
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA



INSTALL:


	a. Local Install
	- clone this repo & unpack
	- cd to directory of repo
	- activate virtual environment (e.g. workon venv1)
	- pip install .


	b. Install directly from github with pip
	- pip install git+https://github.com/dermatty/GINZYENC.git#egg=ginzyenc

	
	c. from PyPi
	- pip install ginzyenc

    d. Gentoo ebuild
    - add dermatty_overlay with layman (see overlay github site for instructions)
    - emerge -a ginzyenc
