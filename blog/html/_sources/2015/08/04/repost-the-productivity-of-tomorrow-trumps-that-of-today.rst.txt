The productivity of tomorrow trumps that of today
=================================================

.. categories:: Programming

.. sidebar:: Editorial note

   I'm republishing this post from my old blog (which is no longer online).
   It's published as it were when I first made it online with only minor
   changes.  But I think I stand by this still.

   Hope you'll enjoy the reading.


That's probably harsh, but I think it is absolutely right.  Doing crappy
software today to be more productive today will make you less productive
tomorrow.  It's this simple.  And that's cumulative too; meaning that if you
neglect your future productivity, it will be slowly diminishing until a point
of negative competitive disadvantage where you'll find yourself struggling to
keep up instead of innovating.

And it's so damn exhausting to explain why...

Software complexity does not come from the tools, but from the mental
framework required (and imposed at times) to understand it.  So don't ever
think measuring Cyclomatic Complexity (CC) and other similar metrics will
yield something close to the `true measure <WTF per minute_>`__ of the
`quality of your code <coding buddy_>`__.

    There are only `two hard things`_ in Computer Science: cache invalidation
    and naming things.

    -- Phil Karlton

::

  def _check(l):
      if len(l) <= 1:
         return l
      l1, l2 = [], []
      m = l[0]
      for x in l[1:]:
         if x <=m :
            l1.append(x)
         else:
            l2.append(x)
      return _check(l1) + [m] +_check(l2)

This code has a nice CC of 4 which is very nice; yet it will take you at least
a minute to figure out what it does.  If only I had chosen to name the
function `quicksort`...

::

    >>> _check([84, 95, 89, 4, 77, 24, 95, 86, 70, 16])
    [4, 16, 24, 70, 77, 84, 86, 89, 95, 95]


A quiz in less than 5 seconds: What does it mean in OpenERP's ORM the
following lines of code?

::

    group.write({'implied_ids': [(3, implied_group.id)]})


This line of code has a CC of 1: as good as it gets, isn't it?  But it's so
darn difficult to read that unless you have your brain wired up to see "forget
the link between this group and the implied_group"...  To be fair there is
someone out there in the OpenERP universe that cared a bit about this::

    # file addons/base/ir/ir_fields.py

    CREATE = lambda values: (0, False, values)
    UPDATE = lambda id, values: (1, id, values)
    DELETE = lambda id: (2, id, False)
    FORGET = lambda id: (3, id, False)
    LINK_TO = lambda id: (4, id, False)
    DELETE_ALL = lambda: (5, False, False)
    REPLACE_WITH = lambda ids: (6, False, ids)

But no one else is using it!

And, yes, it's exhausting going over this.

.. _WTF per minute: http://www.osnews.com/story/19266/WTFs_m
.. _two hard things: http://martinfowler.com/bliki/TwoHardThings.html
.. _coding buddy: http://blog.codinghorror.com/whos-your-coding-buddy/
