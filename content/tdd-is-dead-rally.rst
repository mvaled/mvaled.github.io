TDD is dead rally
=================

:date: 2014-05-27
:category: Programming
:tags: design, tests
:slug: tdd-is-dead-rally

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


Update: Amplification and support to `David's arguments <tdd-is-dead_>`__

The previous words were written just after skimming over several tweets.  I
had read `David's test-induced design damage`_ but I had missed the previous
post `TDD is dead.  Long live testing`__.  So this update is my one cent to
the issue, but I will not discuss about "slow collaborators" but about my
design experience with our `Python Query Language`_.

__ tdd-is-dead_

The test-first mantra assumes too much about how you are going to decompose
your problem.  Let's start with a retrospective account of how this happened
in `xotl.ql`_.

I can detect four distinct stages:

a) The beginnings.  Slightly TDD, but the tests were not always written before
   code.  Since `xotl.ql` is just a language we were not sure about what to
   test.

   The idea of having a `query object`:term: that stands for the expression
   was not totally consolidated.  The components of the query were not
   defined.  This stage was heavily driven by our own writings, like `this one
   <http://xotl-ql.readthedocs.org/en/latest/thoughts.html>`__.

   In this case the "literate" spirit dominated the design process, not the
   testing.  Simply we didn't have a full-stack: ie. the language and the
   `translators <query translator>`:term: so that a query could actually be
   executed.

b) Consolidation of the design.  In this stage several devices were invented
   to cope with implementation difficulties, i.e. the `lack of clear
   boundaries <inner-workings>`:ref: between several sub-expressions in a
   single `query`:term:.

   This was the hardest stage.  Testing was employed to keep track of several
   design decisions.  In this stage made appearance our "Particle Bubble" and
   this was complex enough to deserve a handful of tests.  Although several
   tests did influence the design, they hardly drove it.

c) Then the core was done and we turned to `translation
   <xotl.ql.translation.py>`:mod:.  This stage was mainly TDD cause we
   actually were testing a very TDD friendly layer:  Given this state of the
   world, the following query should return these objects.

d) Our current stage. Although in a long pause, we have decided to wipe out
   our entire design and do reverse engineering of python byte-code to extract
   build the `query object`:term:.

   What is foreseeable is that again a kind of literate driven design is going
   to be king: The core structure of the language (the query AST) is what's
   being designed so, what's the point of asking if the result of calling a
   function with a given query expression is a particular AST if the AST is
   what's needs to be validated not the function itself?  At this point this
   is non-sense.  At a later stage where the AST is stable enough those kind
   of tests would actually make sense: they will protect the query language
   against unintentional API-breaking changes.


Footnotes

.. [#some-are] If I recall correctly, the book by `R.L Graham`, `D.E. Knuth`
   and `O. Patashnik` called "Concrete Mathematics" shows some proofs that
   allow "proof-by-instances".


.. _Hoare: http://en.wikipedia.org/wiki/Tony_Hoare
.. _DAS: https://www.destroyallsoftware.com
.. _tdd-is-dead: http://david.heinemeierhansson.com/2014/tdd-is-dead-long-live-testing.html
.. _Python Query Language: https://github.com/merchise-autrement/xotl.ql
.. _xotl.ql: `Python Query Language`_
.. _David's test-induced design damage: http://david.heinemeierhansson.com/2014/test-induced-design-damage.html

..
   Local Variables:
   ispell-dictionary: "en"
   End: