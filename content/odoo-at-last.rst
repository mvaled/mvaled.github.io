.. _odoo-at-last:

Odoo at last!
=============

:date: 2015-05-26
:category: Management
:tags: Odoo, OpenERP
:slug: odoo-at-last



After several months, we have finally moved from OpenERP to Odoo.  It took
several rounds of testing, finding bugs and incompatibilities in our own
modules and fixing them.


A summary of the process
------------------------

The OpenUpgrade_ project proved to be very complete for us --it had almost
everything we needed:

- The Accounting and Project modules were done.

- The CRM module was not yet integrated into the mainstream repository but a
  `fork by Stefan Rijnhart <@stefan_>`__ had a branch that proved very
  complete for our needs.

We began by merging Stefan's branch into our own clone of the repository.  We
came into a small issue and `fixed it <@57cd439_>`__.  Afterwards, some of our
recurrent events were missing the timezone and the migration failed.  For that
we created the branch `8.0-valid-rrules`_ and it did the job after a couple of
tweeks.

The branch we actually used for the migration is `merchise-8.0`_.  It includes
several commits we had to make for our customs addons to work.  Those commits
are probably too local to be merged back into the upstream.  However, we have
published them should anyone finds them useful.

.. _@57cd439: https://github.com/mvaled/OpenUpgrade/commit/57cd439
.. _@stefan: https://github.com/StefanRijnhart/OpenUpgrade
.. _8.0-valid-rrules: https://github.com/mvaled/OpenUpgrade/tree/8.0-valid-rrules
.. _merchise-8.0: https://github.com/mvaled/OpenUpgrade/tree/merchise-8.0


The menu decomposition
----------------------

The biggest issue we've encountered so far is that after several hours of
operation all the menus stopped working: You clicked the "Leads" menu item and
you got, say, the list of Many2Many fields. (???!!!)

A first inspection showed that all menu items in the HTML were *somehow*
related to the same action id.  Quickly, we truncated the ``ir_ui_menu`` table
and its associated ``ir_model_data`` rows, upgraded the DB and all menus came
to life once more.

The day after, the same problem happened.  Deeper inspection of both the code
and the DB showed the problem lied in the ``ir_values`` table.  That table
relates menu items with actions.  The rows containing this relation showed
nonsense: almost all the menu items were related to "``res_partner,20``".  And
in the UI this was interpreted to be pointing to the action with id 20.

Comparing the table before and after the upgrade showed no problem there.  So
this issue had appeared after the migration itself.

Our previous method of truncating ``ir_ui_menu`` didn't fix this issue cause
the ``ir_values`` rows remained there crippling over and over again.  Besides,
truncating ``ir_ui_menu`` had the unintentional, bad side-effect of removing
every Mail list in our DB.

We're still on the track about how the ``ir.values`` were messed up in the
first place.


The magical 6 tabs
------------------

Our users started to report slowness after a couple of hours of working.
First, we noticed that the call to ``load_needaction`` was taking too long and
find out this call asked for too much it did not need, we `provided a fix
<load_needaction fix_>`__ and some loose benchmarks.  Though this patch needs
to be completed, the slowness was solved... for a moment.

Some users kept reporting the Odoo interface was freezing all the time, even
inviting them to go out and drink a cup of coffee...  But other users were
happy about it after the patch.  Closer inspection showed many of the AJAX
calls were blocking waiting for a socket to be available.

It turned out these users had created a habit of opening several tabs when
they worked with OpenERP.  They kept this kind of behavior, but a couple of
facts worked against them:

- We have installed the Odoo chat.  Many of our users are geographically
  spread, the chat provided an instant and cheaper communication path.

  This feature was, by far, one the reason we moved to Odoo in the first
  place.

  On technical side, the chat works by long polling the server.  In our server
  this connection stays open for about 50s before being dropped (only to be
  reestablished a moment later).

  This means: a tab has always at least a connection open to the server.

- As explained by Ilya Grigorik in `High Performance Networking in Chrome`_,
  browsers make only so many connections to the same combination of scheme,
  host and port.

  In Chrome this number is 6.  In Firefox this can be tuned up or down by
  tweaking the ``network.http.max-persistent-connections-per-server``
  parameter, but the default is 6.

Combining these, it means that after opening about 6 tabs every AJAX call has
to wait up to 50s to be able to even reach the server.

We opted for raising this number in Firefox and to warn users about this.  Our
user base is small enough and the server has yet to achieve any noticeable
load.


Epilogue
--------

That's what our migration to Odoo story has gone so far.  A little bit
stressful at times, specially when the menus went south for the second time,
but I think we have crossed the yellow line now.  Should anything comes I'll
report it.

I'd love to hear (or read) about others, so I can learn from their experience.


Updated 2015-06-03
------------------

`The menu decomposition`_ described above was actually an error in a custom
addon and not related with migration process.

While still using OpenERP, we backported the partner merge feature from Odoo
and made it work in OpenERP.  We even added a fuzzy match feature so that
minor typos were not missed.  Now in Odoo it seems our modifications messed
things up.




.. _load_needaction fix: https://github.com/odoo/odoo/pull/6772
.. _OpenUpgrade: https://github.com/OpenUpgrade/OpenUpgrade
.. _posa: http://www.aosabook.org/en/posa/high-performance-networking-in-chrome.html
.. _High Performance Networking in Chrome: posa_
