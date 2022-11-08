#!/bin/python3

# SMT(P)Fuzz
# A Simple username tester against SMTP to determine local users
# Written by Elliot Warren (github.com/e-war) @elliotwarren

import sys
import re



def connect():
    print("TBC")

def __main__():

# Setup variables
    user_args=[]
    username_list = []
    ip_port = ''
    wordlist_path = ''
# Collect arguments and assign to variables if valid

    for arg in sys.argv:
        user_args.append(arg)
        if re.match(r"(\d+\.\d+\.\d+\.\d+\:\d+)",arg):
            ip_port = arg
        elif re.match(r"(\/[\w]+)+",arg):
            wordlist_path = arg

# Check if variables are assigned + remind user if not
    if("-w" not in user_args):
        print("Please include a username wordlist with -w [path/to/wordlist.txt]")
        return 1
    elif(ip_port == ''):
        print("Please include a hostname + port combination in the form IP/DNS:PORT e.g.(127.0.0.1:25)")
        return 1
    elif(wordlist_path == ''):
        print("Please provide a full path to your wordlist after the -w flag...")
        return 1

# Load wordlist

    try:
        with open(wordlist_path,"r") as wordlist_file:
            username_list = wordlist_file.read().splitlines()
    except FileNotFoundError:
        print("The file path was not valid, please try again")
        return 1
# For x in wordlist make connection + check if valid user

    print(user_args)
    print(username_list)

__main__()