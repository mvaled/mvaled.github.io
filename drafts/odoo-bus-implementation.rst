============================================
 Improving the bus *implementation* in Odoo
============================================

.. categories:: Web Development
.. tags:: HTML5

As I commented on my `post about our migration to Odoo`_, our users open many
tabs to the same Odoo instance.  When the chat is active this means an open
connection for each tab and, since a chat is interactive in nature, all but
one of these connections are not actually required [#notify]_.  This is only
valid cause all those polling connections are `updating the same rows` in the
DB.

A few days ago `I reported`_ that switching from a threaded based deployment
to a forked one (with a gevent_ based process for long polling connections),
actually spiked the concurrency issues we were witnessing in our DB.  Our DB
complained about being unable to *serialize* concurrent transactions.  By
inspecting the logs we noticed that almost always this had to do with an
update to the table ``im_chat_presence``, that holds the status of users in
the chat.

I thought the forked model would diminish the chance of collisions because (I
thought) Odoo would use a single DB connection per worker process and another
one for the gevent worker that would simply serialize *all* the chat related
queries.

This spike was against all rationale I could think of, but honestly I didn't
check my assumptions by reading the code.  They might just be the wrong
assumptions in the first place, and I need to really read the code to see
what's really happening.

After restoring the threaded deployment the concurrency issues dropped again.
They didn't get to the levels they were before, but at the same time we were
introducing other modules (and the related staff), so there are more open
tabs...


It's time to stop the concurrency issues
========================================

There are several questions that need to be answered before making a final
decision in this issue:

- Why does Odoo seems to be using a `serializable isolation level`_\ ?  Or
  does the reported error message is misleading?

- Do we actually keep a single process with a single DB connection when using
  the gevent process?


Notes
=====

.. [#notify] Of course it allows the web app to change the window's title when
   then user has an unread message, but in our case this notification is also
   unneeded, because the message is actually being read in another tab.
