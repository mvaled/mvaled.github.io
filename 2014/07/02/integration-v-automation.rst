===========================
 Integration v. Automation
===========================

.. categories:: OpenERP, Odoo
.. tags:: integration


.. sidebar:: Editorial note

   I'm republishing this post from my `old blog`__.  It's published as it were
   when I first made it online with only minor changes.  I'm planning a follow
   up on the subject and more post about my experiences with Odoo_ (OpenERP).
   That's I deem this repost needed.

   Hope you'll enjoy the reading.

__ http://manuelonsoftware.wordpress.com/2014/05/12/integration-v-automation/


Being an OpenERP bee these days has lead me to think a bit about integration,
how does it happens inside OpenERP, its architecture, assumptions and other
stuff.  In a first iteration I used to think about integration in terms of
integrating two (or more) OpenERP addons, for instance, integrating Sales with
Accounting.  At a very programming-oriented level this reduces, in the current
state of OpenERP, to integrate their modules.  But later, I found out that
this approach is fundamentally flawed and causes many quirks.

This post starts with a tale about one of the many issues we have encounter
when deploying OpenERP in an small enterprise.  Then I will argue about what
integration means.  Lastly, I will turn to automation as a mean for
integration and not the only way to do it.


The Integration tale
====================

I want to start with a simple and very real [#accounting-last]_ use case: Bob
is a salesperson processing a CRM_ lead.

The story beings when Bob opens the lead and clicks on the Edit button and the
first thing he tries to do is to fill the client's contact info because it's a
new client.  He clicks on the edit button besides the "Client" field which
opens a window.  He fills the data and clicks "save", but suddenly it fails
saying that Bob (a salesperson) should have filled the "Account payable" and
"Account receivable" fields.  So Bob says:

  Oh, boy!  What did I do wrong?.  Let's try again...  Nope...  Uh.  What
  should I do?

  Hey!  Peter.  Do you know what's happening here?  This won't let me enter
  this client's contact data, it keeps telling me that these accounts are
  wrong?  What the heck are these accounts anyway?

And Peter has no idea, so he calls Sally who's a very pretty girl that
probably does not have a clue either about what's happening but it's so nice
to have a reason to approach her...  Surprisingly Sally seems to be only one
who actually paid attention to the information meeting that morning and she
says:

  Ah!  This probably has to do with the Accounting module being installed.
  They say they will do that today...  Let's ask Stephanie.


And Stephanie realizes what's happening and fix it somehow.  An hour later Bob
can resume his work and finish processing his CRM lead.

The end.

So, what is wrong with this story?

.. figure:: ./computer_problems.png
   :alt: Computer problems.

   Computer Problems.  Taken from xkcb_.


Depiction of wrongness
----------------------

In my opinion there are two things that are clearly wrong with this:

a) Requiring data *when* it's not required.  When you're in a CRM use case
   requiring accounting-related seems really overstepping.

b) Not being able to issue a request for completion.  Bob should have been
   able to keep working and after the new client was saved a completion
   request should have been sent to those being able to complete the data.

   That completion request might just get ignored, but other use cases (like
   submit an invoice to that client) would actually require the data and thus
   the cycle would be closed after all.

Some would think that this is just a "configuration problem" as we will
`discuss below`__.  But finding that solution took me several dives into the
code and re-parsing of the documentation, so I'll try to walk you through the
process.

__ `On using properties`_


The issue.  The making off
--------------------------

.. warning:: Technical stuff ahead.  Wearing hardhats is mandatory.

By installing the "Accounting & Finance" addon [#v.accountant]_ you touch many
parts of your system besides installing new stuff.  In fact, the module forces
the installation of many other modules, including ``product`` [#no-gnucash]_.

It also modifies the |res.partner| model from the ``base`` addon.  You may
think about the |res.partner| model as an attempt to merge the contact
information for both clients, suppliers and employees into a single
entity [#v.contact-info]_.  It has many fields that comprise name, job
position, contact information, etc...

When you install the ``account`` addon, the |res.partner| gets appended a
whole bunch of other fields, including the said "account payable" and "account
receivable" fields, which are also marked as mandatory:

.. highlight:: python

.. code-block:: python

   'property_account_payable': fields.property(
       'account.account',
       type='many2one',
       relation='account.account',
       string="Account Payable",
       view_load=True,
       domain="[('type', '=', 'payable')]",
       help="This account will be used instead of the default one as the payable account for the current partner",
       required=True),
   'property_account_receivable': fields.property(
       'account.account',
       type='many2one',
       relation='account.account',
       string="Account Receivable",
       view_load=True,
       domain="[('type', '=', 'receivable')]",
       help="This account will be used instead of the default one as the receivable account for the current partner",
       required=True),


This are not actual fields of the model |res.partner|, but properties, which
are "special".


On using properties
~~~~~~~~~~~~~~~~~~~

Properties are of course related to the "solution" for the problem described
above.  But the solution is well hidden under the title of `Database setup`_
in the OpenERP Book.  That's the reason I'm using this case to open the
`OpenERP corner`.  If you deploy CRM before accounting [#accounting-last]_
you'd probably find no interest in reading a topic called "Database setup"...
you have set your database up already, haven't you?

You should notice that both `Account receivable` and `Account payable` are, in
fact, properties (i.e defined via ``fields.property``).  This actually means
that those fields take their default values from a global configuration.

Those values were not properly set in our case cause there were no localized
account chart that applied to our enterprise.  We have to create all the
accounts by hand, and yes, we missed (didn't know) that we have to create
those properties.

Our problem is solved by defining those properties in the configuration menu.

However this workaround is very unsatisfying:

- It involves the administrator of the system because he's the one that has
  access to the "Configuration Parameters".  AFAIK, the accountant
  himself/herself cannot change the defaults, unless you bestow all the powers
  on him/her.

- It does not resolve the integration problem others might present in the
  future.  Integration is harder that having some default values.  For
  instance, Cuban accounting norms establish more than 10 accounts for
  receivables with empty slots for more if needed.  They require to have
  different accounts (receivable and/or payable) for bills to/from people
  (B2C) separated from those bills to/from other enterprises (B2B), and also
  different accounts for long-term and short-terms bills.  The last case
  cannot be decided by just looking at the client or supplier, more
  information about the `economic fact` is needed.

- It does not actually resolve the current integration problem since the
  accountant needs to make sure the "Account Receivable" is the correct one
  for the client and he's not notified when salesman Bob creates a new
  partner.  So, what really happens is that the accountant needs to review
  journal entries and before posting them, and change the account if needed.

.. |res.partner| replace:: ``"res.partner"``


Integration v. Automation
=========================

An ERP should simplify things by *integrating business areas*, shouldn't it?
That's the main driver behind the feature of automatically generating journal
entries.  Under this principle when an invoice is sent to a client a journal
entry should be made recording we should get paid for that, ie.  the client's
account receivable gets increased [#account-normal-balance]_.  Likewise when
we get a supplier invoice, an entry should record that we must pay that bill,
ie.  the supplier's account payable gets increased.

You see now how the "Account Receivable" and "Account Payable" fields for the
partner play their part in the *automation* of the accounting processes.  This
is deeply weaved into the ``account`` module's source code.  Meaning that
there's the assumption that partners have those properties we're talking
about.  And that's true because you have injected them and, if you configured
everything as expected, they have their default values.

Notice the difference between the expectation of *integration* of business
areas and how the integration happens in this case via a very specific kind of
*automation*.

I'll argue that the current state of this design is flawed.  When standards
change and/or are not applicable this kind of automation does more harm that
it helps.

This is the reason the module that controls the "Anglo-Saxon
accounting" [#basis]_ is very difficult to understand and the result
artificial: they need an "interim" account to keep track the different stages.
In the standard (for OpenERP) accounting the event to produce journal items in
the debtor/creditor account is the creation of the invoice.  In the
anglo-saxon scheme the journal should be created at shipping time.

I argue that given another framework that clearly separates every actor and
function will improve how this pattern could be implemented.  I think that
this framework must have:

a) Signals and events.

b) Actors like the accountant, and probably an automated agent for the
   accountant that could do the same the models do right now.  But being
   responsive (ie. they respond to signals) they could be easily bypassed.

Of course there are more things needed. I'm thinking about those two plus the
ones OpenERP already has.

I think that recognizing actors is the major improvement.  Actors are
abstractions about intelligence. If a person should be doing some kind of
intelligent decision (like accountants), then you should encode (in your
design) that decision as being taken by an actor.

Having artificial agents that could take over when the task is standard or
programmable is also an option in this case.  Anywhere in you design an actor
does something, and agent could be replacing the human.  The agents could be
as dumb as the couple of rules we have now: create a journal entry each time
an invoice goes to the valid state, and do it this way.  But agents could be
also provided of machine learning techniques and they could observe the how
the human accountant proceeds when something happened.  Of course this would
require the human to proceed in case-by-case fashion and that's not always
true.

No matter if the machine learning is never done, I argue that designing with
actors and agents will lead to better a implementation, easier to understand,
maintain and evolve.


Notes
=====

.. [#accounting-last] This is no hypothetical at all.  We're actually
   deploying Accounting after having deployed Project Management and CRM_.

   This has come with many surprises but that's what this post is about.

.. [#v.accountant] The word addon in here is important.  There are actually
   two OpenERP addons named "Accounting & Finance": the ``account`` addon and
   the ``account_accountant``.  The second one is flagged as an `application`
   and, thus, it takes a more prominent place in the listing of available
   applications.  Installing the application forces the installation of the
   ``account`` module anyway.

.. [#no-gnucash] That is why I still do my personal (home) accounting with
   `GNU Cash`_.

.. [#v.contact-info] This merge has problems of its own, but that's a matter
   for another post.

.. [#account-normal-balance] Though an account either gets credited or
   debited, I will avoid that accounting-related terms cause it's not needed
   for the argument in this post.  If you need to know, start by knowing that
   receivables have a debit `normal balance`_ and go from there.

.. [#basis]  I'm not quite sure if this "anglo-saxon accounting" refers to
	     different `basis of accounting`_.


.. _CRM: http://en.wikipedia.org/wiki/Customer_relationship_management
.. _xkcb: http://xkcd.com/
.. _xkcb.com: _xkcb
.. _normal balance: http://en.wikipedia.org/wiki/Normal_balance
.. _GNU Cash: http://www.gnucash.org/
.. _basis of accounting: http://en.wikipedia.org/wiki/Basis_of_accounting
.. _Database setup: https://doc.openerp.com/book/1/1_3_Real_Case/1_3_Real_Case_db_setup/
.. _Odoo: http://www.odoo.com/

..  LocalWords:  addon addons OpenERP CRM

..
   Local Variables:
   ispell-dictionary: "en"
   End:
