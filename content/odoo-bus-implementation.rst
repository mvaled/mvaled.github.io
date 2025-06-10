======================================================================
 The bus *implementation* in Odoo and notification systems in the Web
======================================================================

:date: 2015-09-12
:category: Web Development
:tags: HTML5, Odoo
:slug: odoo-bus-implementation



.. sidebar:: Delayed post.

   This post has been delayed for a very, very long time.  If I trust the logs
   in my blog's git repository the post is "finished" since Sat Sep 12, 2015.
   Well, that's not true, and I must really finish it now.

   As it happens, in the meantime, I was not twiddling my fingers and I made
   two "advances" about the bus implementation:

   - I made a successful implementation of a cross-tab bus implementation:
     https://github.com/merchise-autrement/odoo/tree/merchise-8.0-bus-service-worker

   - I discovered that Odoo 9's code base already has the cross-tab feature
     integrated.

I commented on my post about our migration to Odoo that our users open many
tabs to the same Odoo instance.  When the chat is active this means an open
connection for each tab and, since a chat is interactive in nature, all but
one of these connections are not actually required [#notify]_.

A while ago `I reported <twitter-spike-report_>`__ that switching from a
threaded based deployment to a pre-forked processes one with a gevent_ based
process for long polling connections, actually spiked the concurrency issues
we were witnessing in our DB.  Our DB complained about being unable to
*serialize* concurrent transactions.  By inspecting the logs we noticed that
almost always this had to do with an update to the table ``im_chat_presence``,
that holds the status of users in the chat.

I thought the forked model would diminish the chance of collisions because (I
thought) Odoo would use a single DB connection per worker process and another
one for the gevent worker that would simply serialize *all* the chat related
queries.

This spike was against all rationale I could think of, but honestly I didn't
check my assumptions by reading the code.  They might just be the wrong
assumptions in the first place, and I needed to really read the code to see
what was really happening.

After restoring the threaded deployment the concurrency issues dropped again.
They didn't get to the same levels they were before, but, at the same time, we
were introducing other modules (and the related staff), so there are more open
tabs...  Afterwards we went back to the process model, and the issues spiked
again, however in a smaller amount.

Several weeks later I deployed a `patch <Odoo bus patch_>`__ to the Odoo bus
implementation that simply reduced the frequency of polling when the `page is
hidden <Visibility API_>`__.  The concurrency issues were now mostly gone:
from about 3k a day to no more than 50.

We still had unanswered questions regarding the DB connection management in
Odoo.  There were suspicious signs.  For instance reducing the ``db_maxconn``
option to 8 or less made Odoo start complaining about the Connection Pool
being full very often.  We already knew that:

- For each cron worker at least 2 connections are used: one holds the cron job
  locked while the other is used by the job itself.

- The bus (used for the chat) also uses another connection to the DB
  "postgres": Notifications and wake-ups of bus-related events use this
  connection.

The most suspicious sign, however, was that with a pool size of 32, this issue
came from time to time.

Time went by and the issue remained at an acceptable (for us) level of few
dozens per day.  You may say it's too much, but, bear with me, it's reasonable
for our hardware and user base.

Just a few days ago, we realized that issues coming from our gevent-based
process were not being properly reported to our Sentry_.  We `fixed the issue
<xoeuf and raven_>`__ and observed that we're getting about 2.5k DB collisions
per day reports again.  And once more the query the table where most of
collisions happen is 'im_chat_presence'.

As a workaround we simply reduced__ the update rate for that table.  But a
better solutions needed to be found.

__ https://github.com/merchise-autrement/odoo/commit/555b5699b96178d5c87f36c0f692dbe8dcf0facb


Cross-tab polling
=================

By looking better our users' usage pattern, we discovered that users switch
from tab to tab regularly and thus the polling is still high.  So we went down
the path of figuring out a way to have a single polling connection even when
many were opened.

I remembered the Local Storage API and went down to write a simple proof of
concept of listening events of the ``localStorage`` from different tabs.  The
proof of concept yielded good results, and so I turned to Google and search
for "cross-tab communication" and found the tabex_ library.

After that, replacing the implementation of the bus for a new one that was
based on a exchanged between tabs was not very hard.  These are the commits
done in our branch (in reverse topological order as in ``git log``)::

  0555434 * bus: Clarify the channel delay in polls.
  d10a1b5 * bus: Checks for the right state.
  af4a6dc * bus: Add language tag in the documentation.
  636490b * im_chat: Revert "Reduce the presure on im_chat_presence table."
  eda7638 * bus: Don't notify if not in polling state.
  4d09ac6 * web_celery: Use a dedicated bus exchange for jobs.
  84239e3 * im_chat: Beep only in the master tab.
  2cb27da * Improve the bus to allow tab synchronization.

The file |bus.rst|_ contains the new design explained.

A few weeks ago I did the `first merge`__ our 8.0 changes into the 9.0 branch.
On the process I realized that Odoo 9.0's bus was improved and now contains
the a cross-tab communication feature.

__ https://github.com/merchise-autrement/odoo/commit/4690d8d466fe622a1a2449403cc41ae78d4caafe

So probably I end up backporting their implementation into 8.0.

.. _bus.rst: https://github.com/merchise-autrement/odoo/blob/merchise-8.0-bus-service-worker/addons/bus/static/src/js/bus.rst
.. |bus.rst| replace:: ``addons/bus/static/src/js/bus.rst``

Notes
=====

.. [#notify] Of course it allows the web app to change the window's title when
   then user has an unread message, but in our case this notification is also
   unneeded, because the message is actually being read in another tab.

.. _Visibility API: http://www.w3.org/TR/page-visibility/
.. _Odoo bus patch: https://github.com/merchise-autrement/odoo/commit/2abfd5ba28e959dda4d6a127a19b3d939008bc1d
.. _gevent: https://pypi.python.org/pypi/gevent
.. _migrate-to-odoo:  https://mvaled.github.io/blog/html/2015/05/26/odoo-at-last.html
.. _twitter-spike-report: https://twitter.com/mvaled/status/615973409697050624
.. _xoeuf and raven: https://github.com/merchise-autrement/xoeuf/commit/d4b3bb7f0d972f31382aad8e6d1bf37c5a74ce99
.. _lunch time: https://twitter.com/mvaled/status/618944844900143104
.. _Sentry: http://getsentry.com/
.. _Olivier Dony: https://github.com/odony
.. _High Performance Odoo: http://fr.slideshare.net/openobject/performance2014-35689113
.. _tabex: https://github.com/nodeca/tabex
