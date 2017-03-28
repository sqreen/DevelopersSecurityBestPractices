---
title: Safe password storage
language: python
---

Password storage is now mandatory in several standards and is a well-known and solved problem.
Not following the best practices could transform a hack into a nightmare for business and developers.

# TLDR

Don't store password in clear-text, don't use md5, use dedicated algorithms for
hashing password, use a salt per user.

# Vulnerable code

It’s universally acknowledged that it’s a bad idea to store plain-text passwords. The recommandation is to hash them. Here are some examples of **WHAT TO NOT DO**.

```python
from hashlib import md5

def hash_password(password):
    return md5(password)
```

```python
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password, '$2b$12$/msH5YVuJWZTfw.AdfLxS.')
```

```python
import os
from passlib.hash import pbkdf2_sha256

def hash_password(password):
    return pbkdf2_sha256('sha256', password, os.urandom(16), iterations=1)
```

All theses examples are vulnerable, see below why.

# Vulnerability explanation

If an attacker take access to your DB dump, apart from personal informations about your customers, he will try to recover your customers password for two reasons:

* Impersonate your customers and abuse the system, like posting spam with legitimate accounts or use the credits to buy things for themselves.
* Try other websites with the same username / email / password and gain access to more personal infos or worst the email account of your customers.

## Clear-text passwords

First, **YOU SHOULD NEVER STORE PASSWORDS IN CLEAR-TEXT**. If an attacker have access to your database dump, they just need to copy the clear-text password and login with it.

There is known counter-attacks to make the attacker life more difficult.

## Hash functions

> A [Hash function](https://en.wikipedia.org/wiki/Hash_function) is any function that can be used to map data of arbitrary size to data of fixed size. The values returned by a hash function are called hash values, hash codes, digests, or simply hashes. - Wikipedia

They have the property that every data (string, bytes, ...) will always give the same hash.

They are used in every languages for hash tables, caches, finding duplicate records, etc...

## Simples hash functions

Thanks to the hash functions properties, Internet has, for a long time, recommended to use simple hash function like [`MD5`](https://en.wikipedia.org/wiki/MD5) or more recently [`SHA1`](https://en.wikipedia.org/wiki/SHA-1) as hash functions for password. The recommendation is better than storing password in clear-text in the database but attackers quickly found the solution.

It's quite easy and quick to compute the md5 of most common password as the `md5('password')` will always be `5f4dcc3b5aa765d61d8327deb882cf99`. So the use of [rainbow tables](https://en.wikipedia.org/wiki/Rainbow_table) quickly became a valuable tools for hackers. If you see the value `5f4dcc3b5aa765d61d8327deb882cf99` in a data leak, you can look in the rainbow table and it will tell you that the clear-text password is `password`.

Don't trust me? [Go check yourself here](http://hashtoolkit.com/reverse-hash/?hash=5f4dcc3b5aa765d61d8327deb882cf99).

The crack is basically immediate, all the passwords are precomputed, the complexity of cracking your password with md5 or sha1 is basically: `O(1)`.

## Wordlist

The problem with brute-forcing passwords is that you need to have a list of "known" passwords in the first place. It's called `wordlist` and is basically a clear-text file of passwords found in previous hack, it's usually the most common one like `123456` or `qwerty`. The problem is that most users uses these simple password or a combination of it. The estimation are as bad as [50% of password found in leaks are from the top 25% in 2016](https://blog.keepersecurity.com/2017/01/13/most-common-passwords-of-2016-research-study/). Passwords crackers can also apply some mangling rules, like replacing a letter by a number `qw3rty` or mixing the case `QwErTy`.

## Salt

One solution that quickly came is to use [a salt](https://en.wikipedia.org/wiki/Salt_(cryptography)); instead of hashing just the password, you hash the password + a random value that you store. So `md5('password' + 'SalT3D') == 'e7c3b1834297faf1ea92754f41daf14f' != md5('password')`. This solution blocks the [most common rainbow tables](http://hashtoolkit.com/reverse-hash?hash=e7c3b1834297faf1ea92754f41daf14f) but the hackers quickly find a new workaround.

As the salt value is unique for all your passwords, the attacker can generate a rainbow table with your salt value and it became easier as computer power went up and parallelization improved.

With this solution, the attacker needs to generate a rainbow table, augmenting the complexity to crack your passwords to: `O(N)`, N being the number of passwords "knowns".

## Per-user salt

Instead of using a global salt, the solution is to generate a salt per user. The downside is that you have to store the salt value along your passwords to be able to check the password.

In this way the attacker would have to generate a rainbow table per salt value. This quickly raise the complexity of the attacker's work. If you have 100 users and one different salt per user, the attacker would have to compute: `100 (users salt) * 100 (number of password to try) = 10000` hashes for cracking all your customers passwords.

With this solution, the attacker needs to generate a rainbow table per user salt, augmenting the complexity to crack your passwords to: `O(M*N)`, M being the number of customers and N being the number of passwords of a password list.

## Let's slow the world

One solution to counter the augmentation of compute power and [use of GPU to crack passwords](https://blog.elcomsoft.com/2016/07/nvidia-pascal-a-great-password-cracking-tool/) is to use hash functions dedicated to password hashing. They are called [Cryptographic hash function](https://en.wikipedia.org/wiki/Cryptographic_hash_function) that are carefully designed to hash password. They have the same basic property that they are deterministic but they have another property fundamental for hashing passwords, it is infeasible to generate a message from its hash value except by trying all possible messages. It means that if an attacker have an cryptographic hash, it will need to brute-force it, try an enormous amount of password, hash them with your user salt and check if it match.

Simple hashing functions are pretty quick and easy to parallelize, [latest reports](https://gist.github.com/epixoip/a83d38f412b4737e99bbef804a270c40) show up to 200 billion per second, yes **200000000000** hash per second for MD5 and only 68 billion for SHA1.

Algorithms like [BCrypt](https://en.wikipedia.org/wiki/Bcrypt) or [pkbdf2](https://en.wikipedia.org/wiki/PBKDF2) are very well suited for password hashing. They were also designed to be future-proof, the complexity can be tuned at runtime via a number of `iteration`, so if one of these algorithms begin to be fast to crack, double the `iterations` and you should be safe.

Checking back the report, with bcrypt, we are down to 105 thousand hash per second for BCrypt with 5 iterations and *only* 9680 hash per second for pbkdf2 with 1000 iterations and these iterations are pretty low according to nowadays standard.

## Closing thoughts

All these good practices have the objective to slow down an hacker that would have access to your database passwords and try to crack them. There is two complimentary solutions:

- Force users to use strong passwords, they are much much harder to crack, check out this website to see the [complexity of different password](https://howsecureismypassword.net/). `password` is marked as cracked instantly while `uFLXW7UZ2J5L1ICTatzQ` would take **558 QUADRILLION YEARS.** If a password cracker couldn't generate your password from its wordlist and mangling rules, except with trying every possible combination of ascii characters, your users should be safe.
- Use a cryptographic pepper. A pepper is added to the password and the salt before hashing. The big difference is that the pepper is **NOT** stored in the database but somewhere else safe. This way if an attacker access your database, he would need to bruteforce the pepper + the password which would be infeasible.

And don't remember, don't write your own hashing function or compose them without knowing. No `md5(md5('password') + 's')` is not inherently safer.

Here is an graph of cracking time per algorithms:

<iframe width="1312" height="811" seamless frameborder="0" scrolling="no" src="https://docs.google.com/a/sqreen.io/spreadsheets/d/1FGSnq-XKSsDLobCcKHXrVp06dDMQ5CrK9iBtcK-OYd0/pubchart?oid=1761889554&amp;format=interactive"></iframe>

This image has been generated from this [Google Spreadsheet](https://docs.google.com/spreadsheets/d/1FGSnq-XKSsDLobCcKHXrVp06dDMQ5CrK9iBtcK-OYd0/edit#gid=0).

# Not vulnerable code

If you are using Django, just follow the [Django documentation](https://docs.djangoproject.com/en/1.10/topics/auth/passwords/) and use standard Django password hashers.

If you are not using Django, you can use [passlib](https://pypi.python.org/pypi/passlib) which is easily installable, maintained and with a very strong opinion API, like you cannot hash a password without a salt. It also support multi-factor auth which is a very good thing.

# Example of attack

{% include_relative _python/README.md %}

## References:

- [https://blogs.dropbox.com/tech/2016/09/how-dropbox-securely-stores-your-passwords/](https://blogs.dropbox.com/tech/2016/09/how-dropbox-securely-stores-your-passwords/)
