Composing iterator-returning functions
======================================

:date: 2018-08-01
:category: Programming
:tags: Haskell, Python
:slug: composing-iterator-returning-functions

A few days ago I was reviewing a piece of Python code.  I was looking for a
bug, but in the process I found a very interesting function.

The system allows the user to "extend" the structure of Products by providing
more attributes which can be used later on when creating Sale (or Purchase)
Orders.  The Product object is like a class defining the structure, and the
items in Orders are the instances of such classes.

When trying to export a full catalog, each attribute implies a new row in the
spreadsheet file.  To avoid too much coupling, this process was modeled by a
kind of seeded generation of every possible row.  The algorithm started with a
seed instance of a product without any attribute, and then it generated every
possible attribute-complete instance by *composing* several functions that
took a instance and returned a iterator of instances.  Each function deals
with a specific type of attribute, and simply copies those attributes in the
instances being generated.

The function doing the generation of all possible instance was more or less
like this:

.. code-block:: python

   def iter_product(initial, *funcs):
      if not funcs:
         yield initial
      else:
         f, *fs = funcs
         for x in f(initial):
            yield from iter_product(x, *fs)

That definition was OK, but I wondered if I could build just the *composition*
of several functions returning iterators, so that I can reuse it with several
initial objects.


A little incursion in Haskell
-----------------------------

In order to test my Haskell, I did first a Haskell version.  I started by
trying to create a *composition* operator much like the ``(.)`` operator,
which has type:

.. code-block:: Haskell

   (.) :: (b -> c) -> (a -> b) -> a -> c

The type of our composition of iterator-returning functions would be:

.. code-block:: Haskell

   infixr 9 >>.
   (>>.) :: (b -> [c]) -> (a -> [b]) -> a -> [c]


The choice of ``(>>.)`` as the operator will become (I hope) evident.  The
most straightforward implementation and easy to understand is using the
list-comprehension syntax:

.. code-block:: Haskell

   g >>. f = \x -> [z| y <- f x, z <- g y]


Can we generalize this?  Yes! The list is an instance of a Monad_, defined as:


.. code-block:: Haskell

   instance Monad [a] where
       return x = [x]
       m >>= f  = concat (map f m)

And list comprehensions can be easily rewritten using the ``do`` notation:

.. code-block:: Haskell

   (>>.) :: Monad m => (b -> m c) -> (a -> m b) -> a -> m c
   g >>. f = \x -> do{y <- f x; z <- g y; return z}

The monadic ``>>=`` operator is usually called the *bind*.  It's type is

::

   Monad m => m a -> (a -> m b) -> m b

So, I think there's a compact way to write our ``>>.`` operator.  And, now you
may start to see why I chose ``>>.``.

The do notation is just syntax-sugar over using ``>>=`` (or its brother
``>>``).  The rules are given here__.  So let's transform our implementation.
We start we our current definition::

  \x -> do {y <- f x; z <- g y; return z}

__ http://book.realworldhaskell.org/read/monads.html#monads.do

And rewrite the ``do`` two times until there are no more::

  \x -> let s1 y = do {z <- g y; return z} in f x >>= s1

  \x -> let s1 y = (let s2 z = return z in g y >>= s2) in f x >>= s1

Now, we can recall the `eta-conversion rule`_ and see that ``s2 = return``,
so::

  \x -> let s1 y = (g y >>= return) in f x >>= s1

Now we can use the monadic "law" that states the ``m >>= return`` must be
equivalent to ``m``::

  \x -> let s1 y = g y in f x >>= s1


And, once more, the eta-conversion help us to remove the `let`, because
``s1 == g``.  Thus we get:

.. code-block:: Haskell

   (>>.)  :: Monad m => (b -> m c) -> (a -> m b) -> a -> m c
   g >>. f = \x -> f x >>= g

This is as good as I was able to get.  Since we're using ``>>=``, I think this
is the best we can get (i.e. we can't generalize to Applicative_).


Chaining several iterator-returning functions
---------------------------------------------

Now, I can define a ``chain`` function.  It takes a list of several
``a -> m a`` functions and compose them together (from right to left, as
expected):


.. code-block:: Haskell

  chain :: Monad m => [a -> m a] -> a -> m a


My first attempt was:

.. code-block:: Haskell

  chain :: Monad m => [a -> m a] -> a -> m a
  chain []  = return
  chain (f:fs) = f >>. (chain fs)

But, then I realized that's a fold:

.. code-block:: Haskell

  chain :: (Foldable l, Monad m) => l (a -> m a) -> a -> m a
  chain = foldr (>>.) return

And that completes our incursion in Haskell.


Doing the same in Python
------------------------

Going from this Haskell definition of ``chain`` to Python is quite easy.  But
we're not going to work with any possible monad, just lists (iterators,
actually).

.. code-block:: Python

   from functools import reduce

   def iter_compose(*fs):
       if len(fs) == 2:
           # optimize the 'lambda x: [x]' for the *usual* case of 2-args.
           return _compose(*fs)
       else:
           return reduce(_compose, fs, lambda x: [x])

   def _compose(g, f):
      return lambda x: (z for y in f(x) for z in g(y))

We have included ``~xoutil.fp.iterators.iter_compose`` in xoutil_ 1.9.6
and 2.0.6.


.. _Monad: http://book.realworldhaskell.org/read/monads.html
.. _eta-conversion rule: https://wiki.haskell.org/Eta_conversion
.. _Applicative: https://wiki.haskell.org/Applicative_functor
.. _xoutil: https://github.com/merchise/xoutil
