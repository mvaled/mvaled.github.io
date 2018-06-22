=====================================
 Experience report with `parsec.py`_
=====================================

.. categories:: Programming
.. tags:: Python, Monad, Parsing

A detour put in place of an introduction
========================================

I was writing a parser for a very tiny language.  I wanted to finish it soon
and I hoped that the code be self-explanatory.  I wondered if using package
`Parsec for python <parsec.py>`_ would achieve both goals (I wasn't doing for
performance: it's a language for tests).

My first attempt showed failed but I couldn't why.  I thought it was due to
either of:

- My grammar cannot be parsed by parsec.

- This version of parsec__ is just not completed, even unusable for small
  things (yet they provide examples to parse a JSON).


__ `parsec.py`_
.. _parsec.py: https://pypi.org/project/parsec
