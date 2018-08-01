==================================
 A failing fail in the monad list
==================================

.. categories:: Programming
.. tags:: Haskell, Monad

.. sidebar:: Update.

   The question__ was answered in Stack Overflow, and it shows that the title
   of this post is incorrect: The failing ``fail`` is in the *function* monad.

__ stackoverflow-50989541_


I'm following the Real World Haskell book.  In the chapter about Monads, they
create simple example using the list monad compute all pairs of numbers ``(x,
y)`` that such that ``x * y == n`` for a given ``n``.

Their solution is:

.. code-block:: haskell

   multiplyTo :: Int -> [(Int, Int)]
   multiplyTo n = do
	 x <- [1..n]
	 y <- [x..n]
	 guarded (x * y == n) $
	   return (x, y)

   guarded :: Bool -> [a] -> [a]
   guarded True xs = xs
   guarded False _ = []


But I was wondering if I could restate ``guarded`` for any monad.  Since
``fail`` in the list monad is ``fail _ = []``, I though I could do:

.. code-block:: haskell

   guarded :: Monad m => Bool -> m a -> m a
   guarded True = id
   guarded False = fail "skipped"

However this actually fails in ghci::

  *Main> multiplyTo 24
  *** Exception: skipped

I let myself sleep, and this morning I figured there's actually a
small/important difference between ``guarded False _ = []`` and ``guarded
False = fail "..."``

The type of ``guarded False`` is ``Monad m => m a -> m a``.  However the type
of ``fail 'skipped'`` is just ``Monad m => m a``.

Why does ``guarded False = fail "skipped"`` type-checks?  That's an `open
question <stackoverflow-50989541>`_ (as of the time of writing).

If I define ``guarded`` as:

.. code-block:: haskell

   guarded :: Monad m => Bool -> m a -> m a
   guarded True xs = xs
   guarded False _ = fail "skipped"

Or:

.. code-block:: haskell

   guarded :: Monad m => Bool -> m a -> m a
   guarded True = id
   guarded False = \s -> fail "skipped"


Both work correctly.

.. warning:: `fail` is strongly discouraged to use in real world haskell code.


.. _stackoverflow-50989541: https://stackoverflow.com/q/50989541/211280
