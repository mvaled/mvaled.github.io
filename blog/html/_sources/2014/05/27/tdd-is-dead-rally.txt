TDD is dead rally
=================

.. categories:: Programming
.. tags:: design, tests
.. date:: 2014-05-27

These days there's a kind of a rally about "TDD being dead".

Most TDD fan supporters are true that you must have a way to proof your code
works.  Many computer `scientists <hoare_>`__ have done several attempts into
the "proofs of correctness" for a program.  But tests are not always proofs,
some are [#some-are]_.

I think the main argument is about when TDD is too much.  Several `Destroy all
software <DAS_>`__ screencasts show a TDD flow that I simply find it's too
much.  But they are, indeed, screencasts; and they are probably intended to
illustrate a point and not to be followed without deviations.

Nevertheless, I don't like the "TDD is dead" mantra either.  It gives space to
a flame war I'm not willing to get into.  I use tests and that's it.  Tests,
at different, levels may express several concerns I need to keep stable:

a) A public API, for instance, should not change just like that.  At least not
   after you have made the commitment to keep it stable.

   You may even need to test for deprecation warnings being issued when you
   need to change an API.

b) Collaborative in-progress debugging.  This tests allow to express standing
   issues.  Some regression tests fall into this category.

How do you do tests?


.. rubric:: Notes


.. [#some-are] If I recall correctly, the book by `R.L Graham`, `D.E. Knuth`
	       and `O. Patashnik` called "Concrete Mathematics" shows some
	       proofs that allow "proof-by-instances".


.. _Hoare: http://en.wikipedia.org/wiki/Tony_Hoare
.. _DAS: https://www.destroyallsoftware.com
