"""
filio is a tool which:
(i)   checks for broken links & empty files in your pc
(ii)  saves a local copy of the result  in your home dir in json format


Usage:
------

    $ filio or filio [option]
Gives a summary of the diagnosis (i.e print out total number of broken & empty files to your stdout):
    $ filio   example:

    you have : 1200 empty files in your pc

    you have : 81 broken files in your pc
    {'header': 'filio statistics',
    'timestamp': '28 Jul 2019 11:45:15',
    'total_no_of_broken_files': 81,
    'total_no_of_empty_files': 1200,
    'total_harddisk_storage':'Total: 292 GB ',
    'used_storage':'Used: 27 GB ',
    'free_storage': 'Free: 249 GB ',
    'disk_healthy': True }

    navigate to $home/name/.filio/data.json to see a local copy of the stats

Gives a detailed info about the diagnosis (i.e print out all the empty & broken files to your stdout):

    $ filio --diagnose-full
    or
    $ filio -df

Available options are:

    -df or --diagnose full run a diagnosis and print out a detailed information about the broken & empty files
    -sm or --send_mail allows the application to send statistical mails to your. True by default
Note:
-----
the checking process might take a while around 2-3 minutes max depending on the number of files to be iterated through

Contact:
--------
- gibsonruitiari@gmail.com
More information is available at:

- https://pypi.org/project/
- https://github.com/nerdloco/filio

Version:
--------
- filio v1.0.0
"""
import sys

import click
import os
import time


import random
import asyncio
import traceback

home_path = os.getenv("HOME",None)

banner = """

███████╗██╗██╗     ██╗ ██████╗ 
██╔════╝██║██║     ██║██╔═══██╗
█████╗  ██║██║     ██║██║   ██║
██╔══╝  ██║██║     ██║██║   ██║
██║     ██║███████╗██║╚██████╔╝
        
"""


@click.command()
@click.argument('filio')
@click.option('--diagnose_full', '-df', is_flag=True, help='Receive a detailed diagnosis')
def main(filio, diagnose_full):
    from filio.utils import run, detailed_info
    print(banner)
    print(__doc__)
    if diagnose_full:
        with click.progressbar(range(1, 100000), label='Processing please wait',
                               fill_char=click.style('#', fg='green')) as bar:
            for item in bar:
                time.sleep(0.002 * random.random())
        time.sleep(0.1)
        # call the detailed function
        try:
            if home_path is None:
                click.secho("The home_path is not set please set the home path in your terminal")
                sys.exit()
            else:
                click.secho("Working please wait....")
                detailed_info((home_path))
                click.pause('Press any key to exit')
                sys.exit()
        except Exception as e:
            print(e, file=sys.stderr)
            sys.exit()

    else:
        # summary function
        try:
            if home_path is None:
                click.secho("The home_path is not set please set the home path in your terminal")
                sys.exit()
            else:
                with click.progressbar(range(1, 100000), label="Processing please wait",
                                       fill_char=click.style('#', fg='green')) as bar:
                    for item in bar:
                        time.sleep(0.002 * random.random())
                click.secho("Working please wait....")
                loop = asyncio.get_event_loop()
                loop.run_until_complete(run((home_path)))
                loop.close()
                click.secho("Done.....")
                click.pause('Press any key to exit')
        except Exception as e:
            traceback.format_exc()
            print(f"{e} You can raise this issue with the dev here: "
                  f"https://github.com/nerdloco/filio/issues")
            sys.exit()


if __name__ == '__main__':
    main()
