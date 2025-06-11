Dissecting `foldl` in terms of `foldr`
======================================

:date: 2018-01-22
:category: Programming
:tags: Haskell
:slug: foldl-in-terms-of-foldr

The book 'Real World Haskell' provides an implementation of ``foldl`` in terms
of ``foldr``:

.. code-block:: haskell

   myFoldl:: (b -> a -> b) -> b -> [a] -> b
   myFoldl f z xs = foldr step id xs z
      where step x g a = g(f a x)


They ask the reader (me) to try to understand the implementation.  They warn
it's not trivial, but I found it interesting.  So, I just want to share my
line of thought.

The first thing I noticed is that ``z`` is not an argument to ``foldr``; you
can rewrite the first line as:

.. code-block:: haskell

   (foldr step id xs) z


This makes visible that the result of the ``foldr`` is a function that takes
`z` as an argument.  By looking a the case ``foldr step id []``, which equates
to ``id``, we can see that the type of the ``foldr``\ 's result is ``b -> b``.

This also implies that the type of ``step`` must be ``a -> (b -> b) -> (b ->
b)``.  You can prove that by extracting ``step``:

.. code-block:: haskell

   step1 :: (b -> a -> b) -> a -> (b -> b) -> (b -> b)
   step1 f x g a = g(f a x)

   myFoldl1 :: (b -> a -> b) -> b -> [a] -> b
   myFoldl1 f z xs = foldr (step1 f) id xs z


Use `ghci` to verify that.

Now comes the *funny* part of the implementation: ``step`` is defined with
three arguments

.. code-block:: haskell

   where step x g a = g(f a x)


but ``foldr`` only passes the first two, and that's totally fine; the result
will be another function.

You can make this explicit:


.. code-block:: haskell

   myFoldl2 :: (b -> a -> b) -> b -> [a] -> b
   myFoldl2 f z xs = foldr step id xs z
      where step x g = \a -> g(f a x)


That's a beautiful thing about Haskell both definitions of ``step`` are
actually indistinguishable:

.. code-block:: haskell

    step x g a = g(f a x)

    step x g = \a -> g(f a x)

The first one takes an *equation-like* outlook that I find very elegant in a
programming language.


Having all that we can easily follow how the expression ``myFoldl (+) 0 [1,
2]`` would proceed:

.. code-block:: haskell

   myFoldl (+) 0 [1, 2]
   (foldr step id [1, 2]) 0                  -- by def. of myFoldl
   (step 1 (foldr step id [2])) 0            -- by def. of foldr
   (step 1 (step 2 (foldr step id []))) 0    -- by def. of foldr
   (step 1 (step 2 id)) 0                    -- by def. of foldr for []
   (step 1 (\a -> id(a + 2))) 0              -- applying `step 2 id`

   (step 1 (\a -> a + 2)) 0                  -- applying id, Haskell might not
                                                do this right now

   (\x -> (\a -> a + 2)(x + 1)) 0            -- applying step
   (\x -> (x + 1) + 2) 0                     -- applying the inner lambda
   (0 + 1) + 2                               -- applying the outer lambda


And that's (more or less) how ``myFoldl`` works.
