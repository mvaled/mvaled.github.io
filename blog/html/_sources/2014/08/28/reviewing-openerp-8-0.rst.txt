====================
 Reviewing Odoo 8.0
====================

.. categories:: OpenERP, Odoo
.. tags:: review

This is the first of a series of blog posts related to the next OpenERP 8.0
(or should I say Odoo 8.0).  This first post will be very "seeking for
orientation" on major new features and changes.  Don't expect anything to be
deeply commented or analyzed.

I will probably devote several posts for changes in some modules, but in this
one I'll just write about things that can be immediately seen when you first
install it.


Installing Odoo 8.0
===================

I'm working with a clone from the now official `github.com odoo repository`__.
Of course I'm using the branch "8.0" for this review.

__ `odoo at github.com`_

I prepared a `virtual environment`_ and installed odoo there like this::

  $ python setup.py develop

The first I noticed is that several new requirements are in place, and the
`pyPdf` requirement had been forgotten.

Second thing noticed is that unlike the "7.0" you don't need to run the
``openerp-server`` script passing the ``--addons-path=./addons``.  In 8.0 they
include this path automatically.  So running ``./openerp-server`` is enough.

Also the ``python setup.py sdist`` command includes this path as well, so a
properly built distribution from source seems more doable.  I haven't tried
this yet, but I will, cause that was for sure something missing in 7.0.  It's
quite suspicious that the tarball is too small (around 13MB) though.


New addons
==========

Instant Messaging
-----------------

Once I ran the server I installed a demo DB to see what's new.  The first
thing that captured my attention was an "Instant Messaging" module.  I gave it
a try and it seemed to work out-of-box.

It uses the quite old `long polling`_ technique instead of the brand new
HTML5_  `Server-Sent Events`_ (SSE) stuff.  Why?

My first guess was that multi-process deployments would need to pass messages
around between the HTTP processes.  That requires a kind of Inter-Processes
Communication (IPC).  Popular choices for achieving this in web applications
are Redis_ and RabbitMQ_, but then you'd need to setup either for this to
work.

After thinking in this a bit more (actually the thinking about this occurred
at the same time I was writing this post) I realized that the *current*
multi-process deployments would still need this IPC to properly work.  So I
ran ``./openerp-server --workers=2`` and tested it again.  The chat stopped to
work and the following error was logged from time to time:

.. code-block:: traceback

   2014-08-27 22:53:48,972 17858 ERROR o8 openerp.http: Exception during JSON request handling.
   Traceback (most recent call last):
     File "/<..>/odoo/openerp/http.py", line 476, in _handle_exception
       return super(JsonRequest, self)._handle_exception(exception)
     File "/<..>/odoo/openerp/http.py", line 495, in dispatch
       result = self._call_function(**self.params)
     File "/<..>/odoo/openerp/http.py", line 311, in _call_function
       return checked_call(self.db, *args, **kwargs)
     File "/<..>/odoo/openerp/service/model.py", line 113, in wrapper
       return f(dbname, *args, **kwargs)
     File "/<..>/odoo/openerp/http.py", line 308, in checked_call
       return self.endpoint(*a, **kw)
     File "/<..>/odoo/openerp/http.py", line 685, in __call__
       return self.method(*args, **kw)
     File "/<..>/odoo/openerp/http.py", line 360, in response_wrap
       response = f(*args, **kw)
     File "/<..>/odoo/addons/bus/bus.py", line 188, in poll
       raise Exception("bus.Bus unavailable")
   Exception: bus.Bus unavailable

The code explains it all.  This is the method ``ImDispatch.start()`` in file
``addons/bus/bus.py``:

.. code-block:: python
   :emphasize-lines: 8

   def start(self):
       if openerp.evented:
	   # gevent mode
	   import gevent
	   self.Event = gevent.event.Event
	   gevent.spawn(self.run)
       elif openerp.multi_process:
	   # disabled in prefork mode
	   return
       else:
	   # threaded mode
	   self.Event = threading.Event
	   t = threading.Thread(name="%s.Bus" % __name__, target=self.run)
	   t.daemon = True
	   t.start()
       return self

The highlighted line says this won't work in a multi-process deployment.  How
do you get to use the `evented` mode, I don't know.  Probably that's the
default now.

So I need to review this feature more closely before going to production.
It's a nice addition though.

I found they have now a |GeventServer|_ for long polling connections.  And the
implementation of the Instant Messaging Bus (`bus.py`_) can be easily adapted
for desktop-like notifications, updating your message inbox, and many other
features that would benefit from this.


Messaging has gone a bit different
----------------------------------

At this point I tried to send a message from a user to another (to test if the
inbox was updated real-time) and realized that the Messaging addons has lost
the "compose a new message" that was previously accessible from the inbox, let
me show you a picture (7.0 on the right, 8.0 on the left):

.. figure:: odoo-vs-openerp.png

   Odoo is missing the "Compose new message" button.

This commit has some explanation::

  commit 0714b231646bb439b121a6aaa43df32fedcb5e6e
  Author: Thibault Delavallée <tde@openerp.com>
  Date:   Wed Aug 13 14:35:25 2014 +0200

  [FIX] mail: when having only mail installed, do not show any 'share with my
  followers' compose box. This comes only with hr, for the inbox. This was
  probably forgotten when updating the mailboxes hr-goal and hr-related
  gamification / chatter stuff.


I then installed the "Employee directory" addon and the "Share with my
followers" box appeared.

More digging in the logs reveals the following::

  commit e6f8666b521fe8c2522d6e94c0c3def54a5f73ed
  Merge: d57a97d bf3d4a7
  Author: Amit Vora <avo@tinyerp.com>
  Date:   Thu Apr 17 11:41:33 2014 +0200

  [MERGE] [IMP] mail: Inbox usability improvements :
  - notficiation_email_send field, renamed into notify_email, has now 2 values: always or never, in
  order to ease the choice and simplify options.
  - inbox: removed 'compose a new messages or write to my followers', because those 2 options are
  already available. The first one is accessible using the top-right email icon, the second one
  is accessible with the 'write to my followers' text box alread present in the inbox.

However I don't see the mentioned "top-right email icon".  In fact, that icon
is present in 7.0, but not in 8.0.  More digging::

  commit 5209fbc7ed9fcad966ab064654a8a8697142be42
  Author: Antony Lesuisse <al@openerp.com>
  Date:   Mon Jun 30 01:51:40 2014 +0200

  [REM] useless icon send a message

  The action is available from the wall.

Got you!  So, Antony removed the icon cause he thought it was the wall, but
Amit had removed it from the wall cause because of the icon.  These things
happen...

After reverting this commit, the icon is reestablished.  But, then I realized
that the feature, however hidden, is actually there: If you click on the
"Share with ..." and instead of writing your message there, click on the
"expand" icon, then you get the same as pressing the (now missing) email icon.
I think that the icon is required, though, since now the "Share..." box is not
shown until HR is installed, and the email icon allows to send email to
outsiders.  My current employer is willing to remove email in favor of this
messaging module.  This may hold him back.

I'm `raising my hand to vote`_ for the rescue of (at least) the icon.
Redundancy is not always bad when it comes to user interface.


This enough for this post.  I'll keep looking at Odoo and I'll write about it.


.. _Server-Sent Events: http://en.wikipedia.org/wiki/Server-sent_events
.. |GeventServer| replace:: ``GeventServer``
.. _GeventServer: https://github.com/odoo/odoo/blob/master/openerp/service/server.py#L321
.. _bus.py: https://github.com/odoo/odoo/blob/master/openerp/addons/bus/bus.py
.. _long polling: http://stackoverflow.com/questions/11077857/what-are-long-polling-websockets-server-sent-events-sse-and-comet
.. _SSE: http://en.wikipedia.org/wiki/Server-sent_events
.. _HTML5: http://en.wikipedia.org/wiki/HTML5

.. _Redis: http://redis.io/
.. _RabbitMQ: http://www.rabbitmq.com/

.. _odoo at github.com: https://github.com/odoo/odoo
.. _virtual environment: https://pypi.python.org/pypi/virtualenv
.. _raising my hand to vote: https://github.com/odoo/odoo/issues/2042

..
   Local Variables:
   ispell-dictionary: "en"
   End:
