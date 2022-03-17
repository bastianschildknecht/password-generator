# Password Generator
The friendly password generator.

## Introduction
Password Generator is a simple but powerful password generation tool. It is designed to be easy to use and easy to understand.
It can be used for generating passwords for logins, pin codes, and much more.
It even has a handy quiet mode, which will not display any messages but the generated password. 
This can for example be useful when piping the output to other programs or in automation scripts.

## Usage
```console
$ python generate_password.py -h
usage: generate_password.py [-h] [-u] [-l] [-n] [-s] [-q] length

generates a random password with the given length and parameters

positional arguments:
  length            the length of the password to generate

optional arguments:
  -h, --help        show this help message and exit
  -u, --upper-case  include upper case characters
  -l, --lower-case  include lower case characters
  -n, --numbers     include numbers
  -s, --symbols     include symbols
  -q, --quiet       only print password
```

## Examples
Here we generate a password with 14 characters and default parameters:
```console
$ python generate_password.py 14

PASSWORD GENERATOR
==================
No characters specified. Defaulting to upper case, lower case, numbers, and symbols.
With the given parameters, the generated password is one of 100.6 septillion possible passwords.
It will take an attacker approx. 3.2 billion years to brute force the password.
It may be much less with more sophisticated attacks (e.g. rainbow tables).

The generated password is:
td$O8gDxqjYT8R

```

And here we generate a 6 digit pin code for a credit card:
```console
$ python generate_password.py 6 --numbers

PASSWORD GENERATOR
==================
With the given parameters, the generated password is one of 1.0 million possible passwords.
It will take an attacker approx. a moment to brute force the password.
It may be much less with more sophisticated attacks (e.g. rainbow tables).

The generated password is:
176812

```