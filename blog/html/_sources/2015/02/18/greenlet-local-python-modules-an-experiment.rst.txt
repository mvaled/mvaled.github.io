===========================================
Hot-swapping Python modules. An experiment.
===========================================

.. categories:: Python, Programming
.. tags:: isolation, erlang

A new project I'm involved with will *probably* require dozens of servers
running several thousands greenlets_ each.  Top-level greenlets represent jobs
and their children will be individual tasks those greenlets are
coordinating/supervising.

This model, however prototypical, resembles that of the OTP_ in Erlang.  A
greenlet may be either a supervisor or a worker.

But there's something missing in our platform that Erlang do have and that
might yield huge benefits.  You can change your Erlang code while the program
is running.


Modulets.  The idea
-------------------

I asked myself if I could devise an *import mechanism* that would allow to
update a Python module in a way that already-running greenlets stay unaffected
but newly created ones use the new code.

To exemplify, let's say a typical tasks is::

  def receive_confirmation(message, who):
     from jobs.util.email import send_email
     from jobs.util.email import wait_reply
     # Assume both send_email and wait_reply switch away from the current
     # greenlet and only switch back after they are done.
     message = send_email(message, who)
     res = wait_reply(message)
     return res  # this will be sent to the parent greenlet

The servers start and hundreds of this task are launched in different jobs.
Many of them are idle waiting for their replies.  Users are happily getting
their confirmation emails and replying to them (or ignoring them).

However, we start receiving lot of bounces in the postmaster inbox.  Some
users have entered a wrong email address.  A change is in order.

In response, we change our implementation of ``send_email`` so that it does
VERP_ to know which recipients' address are bouncing, and also create a new
`job` that involves receiving confirmation email when a new user registers.

We'd love to simply update our ``jobs.util`` package and be done with it like
this::

  $ source server-virtual-env/bin/activate
  $ pip install -U jobs.util -i https://my.private.server/

New jobs will pick up the new version and the older jobs will keep working as
if nothing would have changed.

That would be really nice.  Such a hot-swap of Python modules per job is what
I'm calling a "modulet".

Currently I have a "working" **yet very experimental and undertested**
implementation of such a mechanism in our `experimental modulets branch`_ in
xoutil.


Modulets in xoutil
------------------

The current implementation is a very early proof of concept and not something
you'd like to put outside your playground.

The file |test_modulet.py|_ is a simple script you may run to see it working.
It simply creates a temporary module ``magic_module`` that has the
``get_magic`` function.  This function returns a single value.

The test launches three greenlets that simply call the ``get_magic`` function
and asserts it returns the "right" magic value.  Between launches the module
gets updated to return a different magic value, which is passed as an argument
to the newly created greenlet.

A single run will print something like::

  $ python test_modulet.py
  Beginning with 3 in /tmp/tmp1d4rK5
  Isolating 'magic_module' as '<greenlet.greenlet object at 0x7f21f4e8daf0>.magic_module'
  Isolating 'magic_module' as '<greenlet.greenlet object at 0x7f21f4e8da50>.magic_module'
  Isolating 'magic_module' as '<greenlet.greenlet object at 0x7f21f4daa7d0>.magic_module'
  Passed. I have the right magic number 1002
  Passed. I have the right magic number 1001
  Passed. I have the right magic number 1000

If you comment the bootstrapping of modulets, then you'll get something like::

  $ python test_modulet.py
  Beginning with 3 in /tmp/tmpeI1oYA
  Wrong magic number
  Traceback (most recent call last):
    File "test_modulet.py", line 49, in rootprog
      g.switch()
    File "test_modulet.py", line 31, in prog
      assert res == magic, "Expected %d but got %d." % (magic, res)
  AssertionError: Expected 1002 but got 1000.
  Wrong magic number
  Traceback (most recent call last):
    File "test_modulet.py", line 49, in rootprog
      g.switch()
    File "test_modulet.py", line 31, in prog
      assert res == magic, "Expected %d but got %d." % (magic, res)
  AssertionError: Expected 1001 but got 1000.
  Passed. I have the right magic number 1000


Future work
-----------

Since we are at the very early stages of this project is not easy to predict
if we'll keep modulets in our platform.  Probably a celery_ based solution be
enough.

If we were to keep it, there are several things to improve:

- The current mechanism pollutes the ``sys.modules`` with a copy of a module
  per top-level greenlet.

  In the current state, this is an ever-growing pile of modules that never
  erases those that are no longer used.

  This needs to be changed in several ways:

  The namespace we use to masquerade the modules need not be (and should not
  be) the repr of the greenlet object.

  For the purposes of isolating different versions of the same code we can
  either use the timestamp of the files, the version of the distribution,
  etc...

  Running a diesel_ server will quickly eat all your RAM unless this is
  changed.

  When a greenlet_ dies the only one informed is its parent.  But we certainly
  don't want jobs to mess with ``sys.modules`` to clean our own mess.

  This poses a challenge of its own and may be delegated outside `xoutil`
  itself.

  That being said, it's likely that the calculation of the current namespace
  and how to dispose of unused modules will be extensions points of
  `modulets`.

- Currently we have a black-list of modules that will never be isolated.

  Changes in those modules will required a restart to be noticed.  Those
  modules are platform-level.  They include `xoutil` itself, `greenlet` and
  the entire standard library (which is not expected to change unless you
  change Python).

  We can also allow white-listing.  Both ways are on the table.

  The white-list imposes more explicit architecture of your platform since it
  requires throughout revision of which modules you're willing to update on
  the run.

  Access to both lists will be a public API of the Modulet Manager.  I can
  envision a remote-control console you'll use to include a new module in the
  white-list.  But that will be an application of the modulet API and included
  in the box.


..
   Local Variables:
   ispell-dictionary: "en"
   End:

..  LocalWords:  greenlets modulets modulet greenlet Erlang OTP VERP

.. _VERP: http://en.wikipedia.org/wiki/Variable_envelope_return_path
.. _OTP: http://www.erlang.org/
.. _greenlet: greenlets_
.. _greenlets: https://greenlet.readthedocs.org/en/latest/
.. _diesel: http://diesel.io/
.. _celery: http://docs.celeryproject.org/en/latest/

.. _experimental modulets branch: modulets_
.. _modulets: https://github.com/merchise-autrement/xoutil/tree/experimental-modulets/xoutil/modules


.. _test_modulet.py: https://github.com/merchise-autrement/xoutil/blob/experimental-modulets/xoutil/modules/test_modulet.py
.. |test_modulet.py| replace:: ``test_modulet.py``
