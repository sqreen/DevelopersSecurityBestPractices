---
title: Safe password storage
language: python
---

Password storage is now mandatory in several standards and is a well-known and solved problem. Not following best practices for password storage could transform a hack into a nightmare for business and developers.

# TL;DR

Don't store passwords in clear-text. Don't hash passwords with MD5. Use dedicated algorithms for hashing passwords. Use a distinct salt per user.

# Vulnerable code

It’s universally acknowledged that storing clear-text passwords is a bad idea. The recommendation is to hash them, using a cryptographically secure hashing algorithm. Here are some examples of **WHAT TO NOT DO**.

```python
from hashlib import MD5

def hash_password(password):
    return MD5(password)
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

All of theses examples are vulnerable; see below why.

# Vulnerability explanation

If an attacker gains access to your database, apart from personal information about your customers, he will try to recover your customers passwords:

* To impersonate your customers and abuse the system, like posting spam using legitimate accounts or using their credits to buy things for themselves.
* To try the passwords on other websites, thereby gaining access to even more personal information or, even worse, taking control of their email account.

## Clear-text passwords

First, **YOU SHOULD NEVER STORE PASSWORDS IN CLEAR-TEXT**. If an attacker gains access to your database, they just need to copy the clear-text password and log in with it.

There are known defences to make the attacker's life more difficult.

## Hash functions

> A [Hash function](https://en.wikipedia.org/wiki/Hash_function) is any function that can be used to map data of arbitrary size to data of fixed size. The values returned by a hash function are called hash values, hash codes, digests, or simply hashes. - Wikipedia

Hash functions have the property that any given input (string, bytes, ...) will always give the same hash as output, and that distinct inputs have a very high probability of producing distinct hashes.

Hashes are used in every language for hash tables, caches, finding duplicate records, etc.

## Simple hash functions

Thanks to the hash function's properties, the Internet has long recommended the use of a simple hash function like [`MD5`](https://en.wikipedia.org/wiki/MD5) or more recently [`SHA1`](https://en.wikipedia.org/wiki/SHA-1) for hashing passwords. The recommendation is better than storing password in clear-text in the database but attackers quickly found a solution.

It's quite easy and quick to compute the MD5 of most common passwords, as `MD5('password')` will always be `5f4dcc3b5aa765d61d8327deb882cf99`. So the use of [rainbow tables](https://en.wikipedia.org/wiki/Rainbow_table) quickly became a valuable tool for attackers. If you see the value `5f4dcc3b5aa765d61d8327deb882cf99` in a data leak, you can look in the rainbow table and it will tell you that the clear-text password is `password`.

Don't trust me? [Go check yourself here](http://hashtoolkit.com/reverse-hash/?hash=5f4dcc3b5aa765d61d8327deb882cf99).

The crack is basically immediate, all possible passwords are precomputed, the complexity of cracking your password with MD5 or sha1 is basically: `O(1)`. Thus, in reality, MD5 is no better than storing passwords in clear-text.

## Wordlist

The problem with brute-forcing passwords is that you need to have a list of "known" passwords in the first place. It's called a `wordlist` and is basically a clear-text file of passwords found in previous hacks, usually the most common ones like `123456` or `qwerty`. The problem is that most users uses these simple password or a combination of them. Security researchers estimate thatas many as [50% of passwords found in leaks are from the top 25% most common passwords in 2016](https://blog.keepersecurity.com/2017/01/13/most-common-passwords-of-2016-research-study/). Passwords crackers can also apply some mangling rules, like replacing a letter by a number `qw3rty` or mixing the case `QwErTy`. So, even with a strong hash, attackers can determine the passwords of many accounts in your system.

## Salt

One solution that quickly came is to use [a salt](https://en.wikipedia.org/wiki/Salt_(cryptography)); instead of hashing just the password, you hash the password concatenated with a random value that you store. So `MD5('password' + 'SalT3D') == 'e7c3b1834297faf1ea92754f41daf14f' != MD5('password')`. This solution blocks the [most common rainbow tables](http://hashtoolkit.com/reverse-hash?hash=e7c3b1834297faf1ea92754f41daf14f) but the hackers quickly found a new workaround.

As the salt value is the same across all the stored passwords, the attacker can generate a rainbow table with your salt value; such computations become easier as computer power increases and parallelization improves.

With this solution, the attacker needs to generate a rainbow table, augmenting the complexity to crack your passwords to: `O(N)`, N being the number of passwords "knowns".

## Per-user salt

Instead of using a global salt, the solution is to generate a salt per user. The downside is that you have to store the salt value along with your passwords to be able to check the password.

In this way, the attacker would have to generate a rainbow table per salt value. This quickly raises the complexity of the attacker's work. If you have 100 users and one distinct salt per user, the attacker would have to compute: `100 (users salt) * 100 (number of password to try) = 10000` hashes to crack all of your customers passwords.

With this solution, the attacker needs to generate a rainbow table per user salt, augmenting the complexity to crack your passwords to: `O(M*N)`, M being the number of customers and N being the number of passwords of a password list.

## Let's slow the world

One solution to counter the augmentation of compute power and [use of GPU to crack passwords](https://blog.elcomsoft.com/2016/07/nvidia-pascal-a-great-password-cracking-tool/) is to use hash functions designed specifically for password hashing. They are called [Cryptographic hash functions](https://en.wikipedia.org/wiki/Cryptographic_hash_function). They have the same basic property in that they are deterministic, but they have another property fundamental for hashing passwords: It is infeasible to generate a message from its hash value except by trying all possible messages. This means that if an attacker has a cryptographic hash, it will need to brute-force it, try an enormous number of passwords, hash them with your user salt, and check if they match.

Simple hashing functions are pretty quick and easy to parallelize, [latest reports](https://gist.github.com/epixoip/a83d38f412b4737e99bbef804a270c40) show up to 200 billion per second, yes **200,000,000,000** hash per second for MD5 and only 68 billion for SHA1.

A slower hashing algorithm can make brute-force attackers harder by forcing them to take longer. Algorithms like [BCrypt](https://en.wikipedia.org/wiki/Bcrypt) or [pkbdf2](https://en.wikipedia.org/wiki/PBKDF2) are very well suited for password hashing because the algorithmic complexity can be tuned at runtime. You can set the number of iterations required to compute a hash, so if one of these algorithms becomes fast to crack, you need only double the iterations, and you should be safe.

Checking back on the report above, with BCrypt, we are down to 105 thousand hashes per second for BCrypt with 5 iterations and *only* 9680 hashes per second for pbkdf2 with 1000 iterations, and these iterations are pretty low according to present standards.

## Closing thoughts

All these good practices have the objective to slow down a hacker that would have access to your database passwords and try to crack them. There are two complimentary solutions:

- Force users to use strong passwords: They are much much harder to crack. Check out this website to see the [complexity of different passwords](https://howsecureismypassword.net/). `password` is marked as cracked instantly while `uFLXW7UZ2J5L1ICTatzQ` would take **558 QUADRILLION YEARS.** If a password cracker couldn't generate your password from its wordlist and mangling rules, except by trying every possible combination of characters, your users should be safe.
- Use a cryptographic pepper. A pepper is added to the password and the salt before hashing. The big difference is that the pepper is **NOT** stored in the database but somewhere else safe. This way if an attacker access your database, he would need to brute force the pepper *and* the password  which would be infeasible.

And please, *do not* write your own hashing function or compose them without understanding what you are doing. And, no, `MD5(MD5('password') + 's')` is not inherently safer.

Here is a graph of cracking time per algorithm:

<iframe width="1312" height="811" seamless frameborder="0" scrolling="no" src="https://docs.google.com/a/sqreen.io/spreadsheets/d/1FGSnq-XKSsDLobCcKHXrVp06dDMQ5CrK9iBtcK-OYd0/pubchart?oid=1761889554&amp;format=interactive"></iframe>

This image has been generated from this [Google Spreadsheet](https://docs.google.com/spreadsheets/d/1FGSnq-XKSsDLobCcKHXrVp06dDMQ5CrK9iBtcK-OYd0/edit#gid=0).

# Non-vulnerable code

If you are using Django, just follow the [Django documentation](https://docs.djangoproject.com/en/1.10/topics/auth/passwords/) and use standard Django password hashers.

If you are not using Django, you can use [passlib](https://pypi.python.org/pypi/passlib) which is easily installable, maintained and with a very opinionated API: For example, you cannot hash a password without a salt. It also support multi-factor auth which is a very good thing.

# Example of attack

{% include_relative _python/README.md %}

## References:

- [https://blogs.dropbox.com/tech/2016/09/how-dropbox-securely-stores-your-passwords/](https://blogs.dropbox.com/tech/2016/09/how-dropbox-securely-stores-your-passwords/)
