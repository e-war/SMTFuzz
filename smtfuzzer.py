#!/bin/python3

# SMT(P)Fuzz
# A Simple username tester against SMTP to determine local users 
# Written by Elliot Warren (github.com/e-war) @elliotwarren

# WARNING: Will only work against targets without authorization for now until implemented
import sys
import re
from telnetlib import Telnet


def invokeSMTPConnection(u,ip_p):
    
# Initialize the connection
    connection = Telnet(ip_p[0],ip_p[1],timeout=3)
    connection.write(b'HELO '+bytes(ip_p[0],"utf-8")+b'\n')

#Decode the correct hostname for VERIFICATION 

    connection.read_until(b'250 ')  #additional space at the end
    hostname = connection.read_until(b'\n').decode("ascii")
    
#For username in user list, verify they exist, append to verified users
    verified_users = []
    for username in u:
        connection.write(b'VRFY '+bytes(username,"utf-8")+b'@'+bytes(hostname,"utf-8")+b'\n')
        connection.read_until(b'252 2.0.0 ')
        verified_users.append(connection.read_until(b'\n').decode("ascii"))
    print("Verified Users:",verified_users.count())
    connection.write(b'exit\n')
    return verified_users

def __main__():

# Setup variables
    user_args=[]
    username_list = []
    valid_usernames = []
    ip_port = ''
    wordlist_path = ''
# Collect arguments and assign to variables if valid

    for arg in sys.argv:
        user_args.append(arg)
        if re.match(r"(\d+\.\d+\.\d+\.\d+\:\d+)",arg):
            ip_port = arg.split(":")
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
        print("Verified user:", username)
# Invoke SMTP connection handler and send username list

    valid_usernames = invokeSMTPConnection(username_list, ip_port)


    if(valid_usernames.count() == 0):
        print("No valid usernames from your wordlist were found.")
    else:
        print("Here is a list of valid usernames i found:")
        for username in valid_usernames:
            print(username)


    print(user_args)
    print(username_list)

__main__()