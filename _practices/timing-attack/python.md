---
title: Timing Attacks against String Comparison
language: python
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

The difference can feels negligible and it's indeed very small but statistics dictates that every small difference can be detected with enough measures. Moreover network jitter is more and more precisely modeled and can be removed from measures over internet. According to [one of the reference paper on the subject](http://www.cs.rice.edu/~dwallach/pub/crosby-timing2009.pdf), "We have shown that, even though the Internet induces significant timing jitter, we can reliably distinguish remote timing differences as low as 20µs".

String comparison is not vulnerable when comparing hashes, not direct user inputs. As hashes fonction are not reversible, knowing that the generated hash first character is the same as the expected one don't give a clue to the cleartext value that the attacker needs to provide.

# Not vulnerable code

The solution to avoid this problem is to compare the two strings in a way that is not dependent to the size of the strings, the algorithm need to take the same amount of time. It's called constant time string comparison.

To do this successfully you must:

 - Compare all of the characters before returning true or false.
    - returning early will leak information
 - Compare strings of equal length
    - if one string is longer or shorter, you'll return early and leak information about string length


Django provides a function [`constant_time_compare`](constant_time_compare) that can be used to securely check two strings.

The python standard lib also provides the function [`hmac.compare_digest`](https://docs.python.org/3/library/hmac.html#hmac.compare_digest) only in Python 3.3+.

# Example of attack

We have provided an example of a vulnerable python web application that checks the token against a hard-coded value.

We also provide a script to remotely try to exploit the timing attack. Don't use this script against a non-owned application.

The script is not good enough to perform a real attack, the application has been made more vulnerable by adding a sleep during the string comparison.


## References:

- [http://www.cs.rice.edu/~dwallach/pub/crosby-timing2009.pdf](http://www.cs.rice.edu/~dwallach/pub/crosby-timing2009.pdf).
- [https://codahale.com/a-lesson-in-timing-attacks/](https://codahale.com/a-lesson-in-timing-attacks/)
- 
