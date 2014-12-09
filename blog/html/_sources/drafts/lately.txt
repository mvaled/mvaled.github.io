What I've been doing lately
===========================

Lately my work has been mainly driven the need to efficiently and smoothly
deploy the Accounting module of OpenERP_ in my employer enterprise.  But at
the same time I'm responsible several development and deployments in the
enterprise.

The accounting-related tasks have made me to study the accounting module, but
also accounting in general from fundamental principles to advanced topics.
Currently I own a collection of 9 books about accounting.  I still have more
studying to do, but now I'm versed enough to the point of being a (very
junior) accounting consultant to the CEO.  This, of course, should yield
future benefits since I'm planning to start a business.

On the technical side, the last week I was doing a final verification of the
module so that the (true) accountant of the enterprise finally migrates to
OpenERP: Taking our QuickBooks files and, with Pentaho Kettle_, migrating the
accounting information to OpenERP, and the comparing the legal reports.  This
has finally yielded good results and we're doing an opening entry to continue
accounting in OpenERP (the enterprise has an accounting period the starts on
Oct, 1st each year).

At the same time a new server for OpenERP and a deployment based on Buildout_
was another one of my tasks.  There's still much to be done and I'm wondering
if Ansible_ would be a good choice to actually manage the deployment since it
involve setting up Postfix_ as the Mail Transfer Agent interfacing OpenERP for
emails.  This means that besides the accounting books I have reviewed several
mail related RFCs (2822_, 2821_ and 2476_ being those I've read the most) and
the Postfix documentation.

The messaging system of OpenERP was, then, another of my targets for
reviewing.  The last thing I found is that OpenERP tries to submit emails
using a From address it does not own without a proper Sender header and,
worse, it sends a "MAIL FROM" command with that same address the MSA should
reject being a foreign one.  This could lead to OpenERP's MTAs being
blacklisted by third parties if a simple address verification is performed.


To fill the gaps, or more precisely: to take breaks from these topics I'm
reading a couple of books and articles:

- High Performance Browser Networking by Ilya Grigorik.

- `Distributed Systems`_

- The `report about Convergent and Commutative Replicated Data Types`_.

- And fur fun, the last book of the Rama trilogy of Arthur Clark and Gentry
  Lee.  Which BTW I've only truly enjoyed the first book.


.. _Distributed Systems: http://book.mixu.net/distsys/ebook.html

.. _OpenERP: http://www.odoo.com/
