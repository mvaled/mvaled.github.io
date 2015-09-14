==================================
 The bus *implementation* in Odoo
==================================

.. categories:: Web Development
.. tags:: HTML5

As I commented on my `post about our migration to Odoo`__, our users open many
tabs to the same Odoo instance.  When the chat is active this means an open
connection for each tab and, since a chat is interactive in nature, all but
one of these connections are not actually required [#notify]_.

__ https://mvaled.github.io/blog/html/2015/05/26/odoo-at-last.html

Some weeks ago `I reported`__ that switching from a threaded based deployment
to a pre forked processes one (with a gevent_ based process for long polling
connections), actually spiked the concurrency issues we were witnessing in our
DB.  Our DB complained about being unable to *serialize* concurrent
transactions.  By inspecting the logs we noticed that almost always this had
to do with an update to the table ``im_chat_presence``, that holds the status
of users in the chat.

I thought the forked model would diminish the chance of collisions because (I
thought) Odoo would use a single DB connection per worker process and another
one for the gevent worker that would simply serialize *all* the chat related
queries.

This spike was against all rationale I could think of, but honestly I didn't
check my assumptions by reading the code.  They might just be the wrong
assumptions in the first place, and I needed to really read the code to see
what was really happening.

After restoring the threaded deployment the concurrency issues dropped again.
They didn't get to the levels they were before, but at the same time we were
introducing other modules (and the related staff), so there are more open
tabs...  Afterwards we went back to the process model, and the issues spiked
again, however in a smaller amount.

A few days ago I deployed a `patch <Odoo bus patch_>`__ to the Odoo bus
implementation that simply reduced the frequency of polling when the `page is
hidden <Visibility API_>`__.

The concurrency issues are now mostly gone: from about 3k a day to no more
than 50.

We're still have unanswered questions regarding the DB connection management
in Odoo.  The are suspicious signs there.  For instance reducing the
``db_maxconn`` option to 8 or less makes Odoo start complaining about the
Connection Pool being full very often.  We already know that:

- For each cron worker at least 2 connections are used: one holds the cron job
  locked while the other is used by the job itself.

- The bus (used for the chat) also uses another connection to the DB called
  "postgres": Notifications and wake-ups of bus-related events use this
  connection.

We don't know yet if other addons try to open other connections to DB.

The most suspicious sign, however, is that with a pool size of 32 we have seen
this issue come from time to time.


Notes
=====

.. [#notify] Of course it allows the web app to change the window's title when
   then user has an unread message, but in our case this notification is also
   unneeded, because the message is actually being read in another tab.

.. _Visibility API: http://www.w3.org/TR/page-visibility/
.. _Odoo bus patch: https://github.com/merchise-autrement/odoo/commit/2abfd5ba28e959dda4d6a127a19b3d939008bc1d
.. _gevent: https://pypi.python.org/pypi/gevent
