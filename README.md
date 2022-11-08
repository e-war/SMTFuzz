# SMTFuzz
### A Simple username tester against SMTP to determine local users
I wrote this tool to fuzz usernames against a [HTB Challenge](https://github.com/e-war/Writeups/tree/master/HackTheBox/Trick) In order to increase my knowledge of fuzzing techniques.

#### Requirements:

- Linux (For now)
- Python 3
    - sys
    - time
    - re
    - telnetlib
    - os

#### Features:
- External wordlists
- DoS disconnection reattemps

#### Usage:
`python3 ./smtfuzz.py -w [wordlist path] (IP/DNS:PORT)`

```
############ FUZZING debian.localdomain ####
# Found 2 /( 189 / 822 )
# Please be patient, this program is slow:
# Trying: LBACSYS
# Verified Users:
#"root@debian.localdomain"

#"BACKUP@debian.localdomain"

We were kicked off this connection, retyring...
```