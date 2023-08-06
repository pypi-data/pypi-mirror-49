About:
------
filio is a tool which:
(i)   checks for broken links & empty files in your pc
(ii)  saves a local copy of the result  in your home dir in json format


Usage:
------
In your terminal type:
    **$ filio or filio [option]**
Gives a summary of the diagnosis (i.e print out total number of broken & empty files to your stdout):
    $ filio   example:

**you have : 1200 empty files in your pc

you have : 81 broken files in your pc
    {'header': 'filio statistics',
    'timestamp': '28 Jul 2019 11:45:15',
    'total_no_of_broken_files': 81,
    'total_no_of_empty_files': 1200,
    'total_harddisk_storage':'Total: 292 GB ',
    'used_storage':'Used: 27 GB ',
    'free_storage': 'Free: 249 GB ',
    'disk_healthy': True }**

**navigate to $home/.filio/data.json to see a local copy of the stats**

Gives a detailed info about the diagnosis (i.e print out all the empty & broken files to your stdout):

   **$ filio --diagnose-full
    or
    $ filio -df**

Available options are:

 **-df or --diagnose full run a diagnosis and print out a detailed information about the broken & empty files**
 
Note:
-----
the checking process might take a while around 2-3 minutes max depending on the number of files to be iterated through

Contact:
--------
For issues/question:

- gibsonruitiari@gmail.com
More information is available at:

- https://pypi.org/project/
- https://github.com/nerdloco/filio

Version:
--------
- filio v1.0.0
