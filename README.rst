senpathylogger
=========

*A commandline tool to get the logs for commercial softwares*

Usage
-----

If you've cloned this project, and want to install the software follow the following steps::

    $ pip install -e .[test]
    $ python setup.py test

To run the project do the following::

    $ senpathylogger accepted --logs=folderName --hosts=hostfile [--out=<outFolder>]
    $ senpathylogger -h | --help