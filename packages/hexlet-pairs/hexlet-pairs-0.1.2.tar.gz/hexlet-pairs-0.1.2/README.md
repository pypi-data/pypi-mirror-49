### hexlet-pairs

A SICP'ish Functional Pairs implemented in Python.

### Usage

<!-- This code will be doctested. Do not touch the markup! -->

    >>> from hexlet import pairs
    >>> p = pairs.cons(42, 'foo')
    >>> pairs.is_pair(p)
    True
    >>> pairs.car(p)
    42
    >>> pairs.cdr(p)
    'foo'
    >>> print(pairs.to_string(p))
    (42, 'foo')
