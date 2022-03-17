# Password Generator
Generates a random password with the given length and parameters.

## Usage
```console
$ python generate_password.py -h
usage: generate_password.py [-h] [-u] [-l] [-n] [-s] length

generates a random password with the given length and parameters

positional arguments:
  length            the length of the password to generate

optional arguments:
  -h, --help        show this help message and exit
  -u, --upper-case  include upper case characters
  -l, --lower-case  include lower case characters
  -n, --numbers     include numbers
  -s, --symbols     include symbols
```

## Example
```console
$ python generate_password.py 10

PASSWORD GENERATOR
==================
No characters specified. Defaulting to upper case, lower case, numbers, and symbols.
With the given parameters, the generated password is one of 3.7 quintillion possible passwords.
It will take an attacker approx. 118 years to brute force the password.
It may be much less with more sophisticated attacks (e.g. rainbow tables).

The generated password is:
L$BIV4ZCOl

```