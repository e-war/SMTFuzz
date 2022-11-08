#!/bin/python3

# SMT(P)Fuzz
# A Simple username tester against SMTP to determine local users 
# Written by Elliot Warren (github.com/e-war) @elliotwarren

# WARNING: Will only work against targets without authorization for now until implemented

# TODO:
import sys
import time
import re
from telnetlib import Telnet
from os import system

def invokeSMTPConnection(ip_p):
    connection = Telnet(ip_p[0],ip_p[1],timeout=20)
    connection.write(b'HELO '+bytes(ip_p[0],"utf-8")+b'\n')
# BUG: NEED TO LET SERVER SETTLE AFTER CONNECT/RECONNECT
    time.sleep(10)
    return connection

def verifyUsers(u,ip_p):
# Initialize variables
    verified_users = []
    expected_connection_codes = [b'250 ',b'220 ']
# 1. Valid user 2. Invalid user 3. Timeout after too many failed connections
    expected_user_codes = [b'252 2.0.0 ',b'550 5.1.1 ',b'421 4.7.0 ']
# Initialize the connection
    connection = invokeSMTPConnection(ip_p)
# This connection process takes a long time right now 
    returned_connection_code = connection.expect(expected_connection_codes)
    if(returned_connection_code[0] == -1):
        raise ConnectionError
    elif(returned_connection_code[0] == 0):
        hostname = connection.read_until(b'\n').decode("ascii")
    elif(returned_connection_code[0] == 1):
        hostname = connection.read_until(b'\n').decode("ascii")
        hostname = re.search(r"^[\w\d\.]+",hostname).group()
    
# For username in user list, verify they exist, append to verified users
    for username in u:
        connection.write(b'VRFY "'+bytes(username,"utf-8")+b'@'+bytes(hostname,"utf-8")+b'"\n')
        returned_user_code = connection.expect(expected_user_codes,timeout=3)
# If timeout die
        if(returned_user_code[0] == -1):
            raise ConnectionError
# If valid, add to verified
        elif(returned_user_code[0] == 0):
                verified_users.append(connection.read_until(b'\n').decode("ascii"))               
# If dos detection die 
        elif(returned_user_code[0] == 2):
            print("We were kicked off this connection, retyring...")
            connection = invokeSMTPConnection(ip_p)
# Show a continous updated list of all verified usernames
        system('/usr/bin/clear')
        print("############ FUZZING "+hostname+" ####")
        print("# Found",len(verified_users),"/(",u.index(username),"/",len(u),")")
        print("# Please be patient, this program is slow:")
        print("# Trying:",username)
        print("# Verified Users:")
        for user in verified_users:
            print("#"+user)
        
    connection.write(b'exit\n')
    return verified_users

def __main__():

# Setup variables
    user_args=[]
    username_list = []
    sanitized_usernames = []
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
# Remove characters which break TELNET requests
    for unsanitised_username in username_list:
        if(re.match(r"[\&\’\`\*\|\/\$\!\@\:\%\(\)\?\"\=\%\{\}\[\]\.\#\~]",unsanitised_username)):
            continue
        else:
            sanitized_usernames.append(unsanitised_username)
    if(len(sanitized_usernames) == 0):
        print("No valid usernames found in that file! Please try again.")
        return 1
# Invoke SMTP connection handler and send username list

    try:
        print("Establishing connection...")
        valid_usernames = verifyUsers(sanitized_usernames, ip_port)
    except ConnectionError:
        print("A connection error such as timeout may have occured, please attemept again after re-establishing connection.")
        return 1


    if(len(valid_usernames) == 0):
        print("No valid usernames from your wordlist were found.")
    else:
        print("Here is a list of valid usernames i found:")
        for username in valid_usernames:
            print(username)
__main__()