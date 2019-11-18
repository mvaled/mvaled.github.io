Why does creating a list comprehension is faster?
=================================================

.. categories:: Programming
.. tags:: Performance, Python

Yesterday, I was removing a list-comprehension as an argument to `sum`:func:.
This is the diff:

.. code-block:: diff

   - sum([p.price for p in self.products])
   + sum(p.price for p in self.products)

To show the original programmer my line of though I performed a little
experiment with the following message and code:

List comprehensions as an argument to *reduce-like* functions are usually less
efficient than using the generation expression itself.  The reason is that
Python creates the list just to discard it afterwards::

	>>> def fib(n):
	...     a, b = 1, 1
	...     while a < n:
	...         yield a
	...         a, b = b, a + b
	...

	>>> %timeit sum([x for x in fib(100)])
	2.61 µs ± 33 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

	>>> %timeit sum(x for x in fib(100))
	3.13 µs ± 18.6 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

I was surprised to see that the list comprehension was a little bit faster
than the generator expression.  So it seems that for short-enough lists, the
implementation of `sum`:func: is quite fast.

I had to change the implementation of `fib` to control the amount of items to
show my point::

  >>> def fib(n):
  ...     a, b = 1, 1
  ...     for _ in range(n):
  ...         yield a
  ...         a, b = b, a + b

An still with 100 items, passing a list is faster::

  >>> %timeit sum(fib(100))
  14.2 µs ± 212 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

  >>> %timeit sum(list(fib(100)))
  16.4 µs ± 247 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

  >>> %timeit sum([x for x in fib(100)])
  18 µs ± 160 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

Of course the differences are too small to draw final conclusions.  And, of
course, as the list grows larger it becomes slower::

  >>> %timeit sum([x for x in fib(10**5)])
  497 ms ± 84.4 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

  >>> %timeit sum(x for x in fib(10**5))
  329 ms ± 17.3 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


So I think I still prefer the version using the generation expression just to
cover my self from the case where there are too many items to be held in
memory.

(I didn't push the commit, though.)
