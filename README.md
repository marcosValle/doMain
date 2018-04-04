```
######################################

              #     #
#####   ####  ##   ##   ##   # #    #
#    # #    # # # # #  #  #  # ##   #
#    # #    # #  #  # #    # # # #  #
#    # #    # #     # ###### # #  # #
#    # #    # #     # #    # # #   ##
#####   ####  #     # #    # # #    #

######################################

usage: run.py [-h] [-t THREADS] [-f FILE] [-ns NAMESERVER] [-o OUTPUT]
              [-e EMAIL] [-s]

optional arguments:
  -h, --help            show this help message and exit
  -t THREADS, --threads THREADS
                        number of threads
  -f FILE, --file FILE  path of file containing the targets
  -ns NAMESERVER, --nameserver NAMESERVER
                        nameserver to query
  -o OUTPUT, --output OUTPUT
                        output file
  -e EMAIL, --email EMAIL
                        generate possible admin emails
  -s, --status          check domains status
```

# About doMain

`doMain` is a multithreaded python3 tool designed to generate information like admin emails or status of domains by querying DNS servers using third party databases.

# Installation

This tool was developed for python3.

    git clone https://github.com/marcosValle/doMain.git

We strongly recommend using a virtualenv. After cloning:

    pip install -r requirements.txt

# Examples

Retrieve domains that point to a nameserver:

    ./run.py -ns ns1.mynameserver.com

Retrieve domains that point to a nameserver using 20 threads:

    ./run.py -ns ns1.mynameserver.com -t 20

Generate possible admin emails from a list of domains:

    ./run.py -f domains.txt -e emails_admin.txt -o result.txt


# Contributing

Feel free to contribute or file an issue. Some suggestions of what could be done to improve this tool:

* Include other DNS databases
* Comparing and consolidating the results of multiple databases
* Reverse DNS lookup

# Disclaimer

This tool and its developers are just users of external APIs. This tool should be used responsibly and comes with no guarantees.
