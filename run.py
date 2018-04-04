#!/usr/bin/env python

import requests
from threading import Event, Thread
import argparse
from testStatus import *

def readRawTargets(fpath):
    with open(fpath, 'r') as f:
        domains = f.readlines()
    return domains

def splitChunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def queryNs(fpath, ns):
    print("Querying nameserver: {}".format(ns))
    r = requests.get('https://api.hackertarget.com/findshareddns/?q='+ns)
    with open(fpath, 'w') as f:
        f.write(r.text)

def checkStatusfromFile(fpath, threads, outputFile):
    targets = readRawTargets(fpath)
    chunks = list(splitChunks(targets, int(len(targets)/threads)))

    ready = Event()
    threads = map(lambda t: TestStatus(t, 'part-'+str(t), list(chunks)[t], outputFile, ready), range(0, threads))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    ready.wait()

def genAdminEmails(targetsPath, emailsPath, outputPath):
    domains = readRawTargets(targetsPath)
    f = open(outputPath, 'w')
    for domain in domains:
        if 'https://' in domain:
            domain = domain[7:]
        if 'http://' in domain:
            domain = domain[6:]
        if 'www.' in domain:
            domain = domain[4:]

        prefixes = readRawTargets(emailsPath)
        for prefix in prefixes:
            prefix = prefix.replace('\n','')
            print(prefix+'@'+domain, end="")
            f.write(prefix+'@'+domain)
    f.close()

def printBanner():
    banner = """
######################################

              #     #
#####   ####  ##   ##   ##   # #    #
#    # #    # # # # #  #  #  # ##   #
#    # #    # #  #  # #    # # # #  #
#    # #    # #     # ###### # #  # #
#    # #    # #     # #    # # #   ##
#####   ####  #     # #    # # #    #

######################################
"""
    print(banner)

def menu():
    printBanner()
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--threads", type=int, default=4,
                                help="number of threads")
    parser.add_argument("-f", "--file",
                                help="path of file containing the targets")
    parser.add_argument("-ns", "--nameserver",
                                help="nameserver to query")
    parser.add_argument("-o", "--output", default='result.txt',
                                help="output file")
    parser.add_argument("-e", "--email",
                                help="generate possible admin emails")
    parser.add_argument("-s", "--status", action="store_true",
                                help="check domains status")


    args = parser.parse_args()

    fpath = ''
    if args.file:
        fpath = args.file
    elif args.nameserver:
        fpath = 'queriedTargets.txt'
        nsTargets = queryNs(fpath, args.nameserver)
    else:
        parser.print_help()
        parser.exit()

    if args.status:
        checkStatusFromFile(fpath, args.threads, args.output)

    if args.email:
        genAdminEmails(fpath, args.email, args.output)

if __name__ == '__main__':
    m = menu()
