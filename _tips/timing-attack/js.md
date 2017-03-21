---
title: Timing Attacks against String Comparison
language: node
---

Timing Attacks are a particular type of attacks that use flaws in code that impact the execution time.

# TLDR

Don't use string comparison `==` when checking for secrets or token equality. Use safe implementations.

# Vulnerable code

For example take this Python code:

```python
def is_authorized(token):
    if token == 'MY_SECURE_TOKEN':
        return True
    else:
        return False
```

# Vulnerability explanation

While being very simple, it's vulnerable. Why? The code that compares two string is equivalent to this one:

```python
def str_equals(first_string, second_string):
    if len(first_string) != len(second_string):
        return False

    for c1, c2 in zip(first_string, second_string):
        if c1 != c2:
            return False

    return True
```

It iterates on each character of the two string and return `False` as soon as two characters are different.

SCHEMA

# Not vulnerable code

Django provides a function [`constant_time_compare`](constant_time_compare) that can be used to securely check two strings.

The python standard lib also provides the function [`hmac.compare_digest`](https://docs.python.org/3/library/hmac.html#hmac.compare_digest) only in Python 3.3+.

# Example of attack

We have provided an example of a vulnerable python web application that checks the token against a hard-coded value.

We also provide a script to remotely try to exploit the timing attack. Don't use this script against a non-owned application.

The script is not good enough to perform a real attack, the application has been made more vulnerable by adding a sleep during the string comparison.


## References:

- [https://codahale.com/a-lesson-in-timing-attacks/](https://codahale.com/a-lesson-in-timing-attacks/)
- 
