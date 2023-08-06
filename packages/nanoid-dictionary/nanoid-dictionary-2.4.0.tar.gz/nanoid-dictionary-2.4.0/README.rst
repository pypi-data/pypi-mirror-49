Nano ID dictionary
******************

Alphabets and string functions designed to be used with `Nano ID <https://github.com/puyuan/py-nanoid>`__.

Installation
============

.. code:: bash

    pip install nanoid-dictionary

Usage
=====

Available alphabets and functions:

* ``alphabet_std``
* ``human_alphabet``
* ``lookalikes``
* ``lowercase``
* ``numbers``
* ``prevent_misreadings(unsafe_chars, alphabet)``
* ``uppercase``

``prevent_misreadings(unsafe_chars, alphabet)`` accepts a string and removes all the characters that look similar by default. The function is also case-insensitive.

.. code:: python

    from nanoid_dictionary import *

    alphabet_std   # => _-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    human_alphabet # => _-23456789abcdefghijkmnpqrstuvwxyzABCDEFGHIJKMNPQRSTUVWXYZ

    lookalikes                               # => 1l0o
    lowercase                                # => abcdefghijklmnopqrstuvwxyz
    numbers                                  # => 0123456789
    prevent_misreadings(lookalikes, 'a1l0o') # => a
    uppercase                                # => ABCDEFGHIJKLMNOPQRSTUVWXYZ

Thanks to
=========

* Andrey Sitnik for `Nano ID <https://github.com/ai/nanoid>`__.
* Aleksandr Zhuravlev for incredible `Nano ID calculator <https://zelark.github.io/nano-id-cc>`__.
