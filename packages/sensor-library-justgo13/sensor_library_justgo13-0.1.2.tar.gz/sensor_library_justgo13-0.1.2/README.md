Sensor project
==============
Using the library
-----------------
**Installation:** 

Enter the command: *pip install sensor-library-justgo13* 

**Testing code:**

Run *test.py* to test parser files of X4 and TI radars and threshold functions of X4 radar.

**Reading documentation:**

Open file */docs/build/latex/sensor_new.pdf*

**Running library GUI**

Run *lidar_gui.py* in terminal after importing library

Sphinx Documentation
--------------------
This project was documented using Sphinx with Vim as the text editor. Sphinx creates .rst
files when initializing project and Vim is used to open and write to these .rst files. A link to download the version
of Vim used in this project can be found here:
 
[Download Vim](https://www.vim.org/download.php#pc)

Sphinx syntax can be be learned through this resource:

[Learn sphinx documentation syntax](https://pythonhosted.org/an_example_pypi_project/sphinx.html)

To initialize a sphinx documentation project use command: *sphinx-quickstart*. Make sure to 
enable autodocs to import auto-generated code. Example of autodoc commands are *automodule, autoclass and
autofunction.*

To build a final project use command *make html* for html pages and *make latex* for latex documents.

Jupyter Notebook
----------------
This project has a Jupyter notebook to demonstrate the results of the X4 parser and threshold functions as well as 
the results of running the TI radar parser. The notebook also shows the results of running the lidar data extraction functions

Running Ouster OS1 Lidar
-------------------------
To run the OS1 Lidar, user must have working version of Ubuntu 16.04 or higher. All documentation 
regarding building and running the Lidar software can be found in the documentation pdf file. 