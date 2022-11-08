# SMTFuzz
### A Simple username tester against SMTP to determine local users
I wrote this tool to fuzz usernames against a [HTB Challenge](https://github.com/e-war/Writeups/tree/master/HackTheBox/Trick) In order to increase my knowledge of fuzzing techniques.

#### Requirements:

- Linux (For now)
- Python 3:
    - 

#### Usage:
`python3 ./smtfuzz.py -w [wordlist path] (IP/DNS:PORT)`