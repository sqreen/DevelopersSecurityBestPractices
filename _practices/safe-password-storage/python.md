---
title: Safe password storage
language: python
---

Password storage is now mandatory in several standards and is a solved problem.
Not following the best practices could make the hacker life very easy to recover clear-text password after a leak.

# TLDR

Don't store password in clear-text, don't use md5, use dedicated algorithms for
hashing password, use a salt per user.

# Vulnerable code

Storing password in clear-text is a bad idea. The recommandation is to hash them. What about this?

```python
from hashlib import md5

def hash_password(password):
    return md5(password)
```

The problem is that md5 is very quick to compute, `hashlib.md5('my_safe_password').hexdigest` takes 716 ns on a modern laptop. You want a slower algorithm:

```python
from passlib.hash import pbkdf2_sha256

def hash_password(password):

```


# Vulnerability explanation

# Not vulnerable code

If you are using Django, just follow the [Django tutorial](https://docs.djangoproject.com/en/1.10/topics/auth/passwords/) and use standard Django password hashers.

# Example of attack

## References:

- [https://blogs.dropbox.com/tech/2016/09/how-dropbox-securely-stores-your-passwords/](https://blogs.dropbox.com/tech/2016/09/how-dropbox-securely-stores-your-passwords/)
