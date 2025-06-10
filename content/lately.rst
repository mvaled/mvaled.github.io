What I've been doing lately
===========================

:date: 2014-12-27
:slug: lately

Lately my work has been mainly driven by the need to efficiently and smoothly
deploy the Accounting module of OpenERP_ in my employer enterprise.  But at
the same time I'm responsible of several development and deployments in the
enterprise.

The accounting-related tasks have made me to study the accounting module, but
also accounting in general from fundamental principles to advanced topics.  I
currently own a collection of 9 books about accounting.  I still have more
studying to do, but now I'm versed enough to the point of being a (very
junior) accounting consultant to the CEO.  This, of course, should yield
future benefits since I'm planning to start a business.

On the technical side, the last week I was doing a final verification of the
module so that the (true) accountant of the enterprise finally migrates to
OpenERP: Taking our QuickBooks files and, with Pentaho Kettle_, migrating the
accounting information to OpenERP, and comparing the legal reports.  This has
finally yielded good results and we're doing an opening entry to continue
accounting in OpenERP (the enterprise has an accounting period the starts on
Oct, 1st each year).

At the same time a new server for OpenERP and a deployment based on Buildout_
was another one of my tasks.  There's still much to be done and I'm wondering
if Ansible_ would be a good choice to actually manage the deployment since it
involve setting up Postfix_ as the Mail Transfer Agent interfacing OpenERP for
emails.  This means that besides the accounting books I have reviewed several
email related RFCs (2822_, 2821_ and 2476_ being those I've read the most) and
the Postfix documentation.

To fill the gaps, or more precisely: to take breaks from these topics I'm
reading a couple of books and articles:

- High Performance Browser Networking by Ilya Grigorik.

- `Distributed Systems`_

- The `report about Convergent and Commutative Replicated Data Types`__ of
  Marc Shapiro and others.  RR-7506, pp. 50 <inria-00555588>.

- And for fun, the last book of the Rama saga of Arthur Clark and Gentry Lee.
  Which BTW I've only truly enjoyed the first book.


Things left in the attic
------------------------

At the beginning of 2014 I expected I could dedicate myself to finish
`xotl.ql`_ by August.  This was, however, not possible.  I still keep my eye
on the topic from time to time, but this needs a lot of time to actually make
a breakthrough.


__ CRDT_

.. _Distributed Systems: http://book.mixu.net/distsys/ebook.html
.. _OpenERP: http://www.odoo.com/

.. _2822: http://tools.ietf.org/html/rfc2822
.. _2821: http://tools.ietf.org/html/rfc2821
.. _2476: http://tools.ietf.org/html/rfc2476
.. _Postfix: http://www.postfix.org/
.. _xotl.ql: https://github.com/merchise-autrement/xotl.ql
.. _Ansible: https://github.com/ansible/ansible
.. _Buildout: https://pypi.python.org/pypi/zc.buildout/
.. _CRDT: https://hal.inria.fr/inria-00555588
.. _Kettle: http://community.pentaho.com/projects/data-integration/

..
   Local Variables:
   ispell-dictionary: "en"
   End:
