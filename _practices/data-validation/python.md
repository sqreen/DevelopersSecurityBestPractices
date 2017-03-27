---
title: Data validation
language: python
---

> Failures or omissions in data validation can lead to data corruption or a security vulnerability. Data validation checks that data are valid, sensible, reasonable, and secure before they are processed. -- [Owasp](https://en.wikipedia.org/wiki/Data_validation#Validation_and_security)

# TLDR

Validate all your input, check the boundaries and the expected types!

# Vulnerable code

Here is an example of python web-service that doesn't check the type of its parameters

```python
@app.route('/category/', methods="POST")
def get_articles_by_category():
    category = request.get_json()['category']
    if category == 'drafts':
        return []

    return pymongo.MongoClient().test.articles.find({'category': category})
```

This endpoint forbid access to the `drafts` category but forget to validate the json request.

# Vulnerability explanation

When we develop code, we often limit our reflexion to the *happy path*. What are the expected inputs and expected outputs. We test them with unittests and move on to the next piece of code.

But even the simplest piece of code could crash when playing with the inputs:

```python
from decimal import Decimal

def decimal_division(number_1, number_2):
    return Decimal(number_1) / Decimal(number_2)
```

It takes two numbers, convert them into Decimal and return the division.

It works great with int and floats:

```python
>>> decimal_division(1, 0.5)
Decimal('2')
```

There is the well-known edge-case:

```python
>>> decimal_division(1, 0)
    ...
    raise error(explanation)
decimal.DivisionByZero: x / 0
```

That is easy to check:

```python
from decimal import Decimal

def decimal_division(number_1, number_2):

    if number_2 == 0:
        raise ValueError(number_2)

    return Decimal(number_1) / Decimal(number_2)
```

What about with non-numbers?

```python
>>> decimal_division(1, None)
    ...
    raise TypeError("Cannot convert %r to Decimal" % value)
TypeError: Cannot convert None to Decimal
```

We should check for inputs types:

```python
from decimal import Decimal

def decimal_division(number_1, number_2):

    if not isinstance(number_1, (int, float)):
        raise ValueError(number_1)

    if number_2 == 0 or not isinstance(number_2, (int, float)):
        raise ValueError(number_2)

    return Decimal(number_1) / Decimal(number_2)
```

But it's not sufficient, we can also trick the boundaries of the arguments we send:

```python
>>> decimal_division(float('inf'), float('-inf'))
    ...
    raise error(explanation)
decimal.InvalidOperation: (+-)INF/(+-)INF
```

We should also limit the values we accept.

```python
from decimal import Decimal

BLACKLIST = [Decimal('inf'), Decimal('-inf')]

def decimal_division(number_1, number_2):

    if not isinstance(number_1, (int, float)) or number_1 in BLACKLIST:
        raise ValueError(number_1)

    if number_2 == 0 or not isinstance(number_2, (int, float)) or number_2 in BLACKLIST:
        raise ValueError(number_2)

    return Decimal(number_1) / Decimal(number_2)
```

# Not vulnerable code

There is severals Python libraries that can helps you validate your inputs:

- Django provides validation through [Forms](http://djangobook.com/form-validation/) and [Models](https://docs.djangoproject.com/en/1.10/ref/models/instances/#validating-objects), be sure to use them.
- [Cerberus](http://cerberus.readthedocs.io/en/latest/) is a clean and nice libraries which is input and validation format agnostic, give it two dicts, it will raise if it fails.

# Example of attack

{% include_relative _python/README.md %}

## References:

- http://www.ibm.com/developerworks/library/l-sp2/index.html
