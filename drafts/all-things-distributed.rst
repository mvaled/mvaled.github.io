========================
 All things distributed
========================

.. categories:: Programming, Thoughts

In the `Riak Handbook by Mathias Meyer <riak-handbook_>`__ there a
first definition of a distributed system:

   "By distributed systems I'm referring to systems that use more
   than one computer, a node, to get a job done"

By this definition even a simple website may simply be distributed
by having a computer for the DB, another for the web application
itself, and (if needed) another computer for the SMTP server that
sends emails on behalf of the site.

Of course, all of that software (the DB, the web app and the mail
server) could be stuffed into a single box and now the system is not
distributed... Not quite right, isn't it?

This definition does not satisfy our intuition about what a
distributed system is.  By it everything is.

When does my system is a distributed system?  Put it differently:
when do I need to make my system a distributed one?  Is it only when
the capacity of a single node is depleted and another node is
required?  Does my DB and application boxes count as separate nodes?

The answer to that question requires a clear definition of what a
distributed system is, or the benefits to design your system as a
distributed system.

Though I don't pretend to give a definition in this post, I will
argue that many information system should follow distributed
patterns.  In fact, I will argue that ERP systems are going to
collapse unless integration is done with distribution in mind.

..
   Local Variables:
   fill-column: 68
   End:
