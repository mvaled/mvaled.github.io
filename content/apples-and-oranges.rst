Apples and Oranges.  How books can mislead our thinking process.
================================================================

:date: 2014-12-09
:category: Book Reviews
:slug: apples-and-oranges

I've just began to read the book "Twisted Network Programming"... Twisted_ is
a popular framework for networking programming.  However, I'd probably skim
most of the Book.  I'm sorry... But as it happens, in the second page of the
second chapter (the one that I began with) they show an illustration on
"Comparing single-threaded, multithreaded, and event-driven program flow".

Hum... `apples and oranges`_.  I mean the thread model of a program will have
some impact on how events are dealt with, but are they truly comparable or the
sole responsibles for the program flow?

Diesel_ is usually ran in a single thread and so is Tornado_.  You may, of
course, run programs written with them in multiple processes (or threads) to
avoid contention when the volume of clients (events) is too high.

Even with a single thread most of the time the system is waiting for the IO
buffers to have data, so they can be classified as event-driven: They actually
response to events.

But what really bothers about this illustration is not that it compare two
thing that could be (and should be made) complementary.  What bothers me is
that the picture tries to fool me by showing that event-driven programs don't
have any "gaps" of idle time between tasks, while the threaded models do.  And
that's simply dishonest.

Probably this is not what the authors meant, and I'm probably going prejudiced
just because of this wrong picture. However, I go to a book like this not for
pleasure but for information.  Finding a piece of data that is not trustworthy
raises a flag and I start to read with a magnifying glass... And that's not
fun either.

Don't expect me to finish this book.

.. rubric:: Update of a couple of hours later...

A few lines below the illustration of matters, they actually say:

  "The event-driven version of the program interleaves the execution of the
  three tasks, but in a single thread of control."

So, let's give it another try.


.. _apples and oranges: http://en.wikipedia.org/wiki/Apples_and_oranges
.. _Twisted: http://www.twistedmatrix.com/
.. _Tornado: http://www.tornadoweb.org/
.. _Diesel: http://diesel.io/

..
   Local Variables:
   ispell-dictionary: "en"
   End: