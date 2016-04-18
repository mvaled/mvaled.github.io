======================================================
 Business rules: A case about coding standards/issues
======================================================

.. categories:: Programming
.. tags:: Odoo


How do you express a business rule in your code?  Would you recognize it a
separate thing that you may or may not use?  For instance, how would you
encode the following rule:

   Whenever you send a customer an invoice for something you have sold to
   him/her, you must create an entry in the "Sales" Journal with the following
   two items (schematic):

::

   Accounts          | Debits            |   Credits
   ------------------+-------------------+-------------------
   Receivable        | $ XXXX            |
   ------------------+-------------------+-------------------
            Sales    |                   |  $ XXXX
   ------------------+-------------------+-------------------


The accountant that told you that made several assumptions:

a) There is a single or definite "Sales" journal.

b) There is a single or definite "Receivable" account.  Or you'll be using an
   Auxiliary Ledger to keep trap of Receivables.

c) There is a single or definite "Sales" account.


__ http://en.wikipedia.org/wiki/Debits_and_credits#T-accounts

Then she will tell you that:

   Whenever you receive payment for an invoice you must create an entry in the
   "Bank" journal with the following two items (schematic):

::

   Accounts          | Debits            |   Credits
   ------------------+-------------------+-------------------
   Bank              | $ XXXX            |
   ------------------+-------------------+-------------------
         Receivable  |                   |  $ XXXX
   ------------------+-------------------+-------------------

She will probably explain that this entry somehow "cancels" the previous one,
so that now you know you should not must claim any further payment for those
"$ XXXX" you were entitled to collect.

Compare those rules with the following:

  For a single (journal) entry to be valid, the sum of the debits of all its
  lines must be equal to the sum the credits.

Is this the same kind of rule?  Obviously not.  The first ones state how you
should generate an entry in the face of a business case.  The last one
indicates which entries are valid no matter what they should record.  In fact,
the first two rules must ensure they generate entries that comply with the
later.

Therefore, I won't call this last one a *rule* anymore, it's kind of an
accounting law [#double-entry]_.  Yes, probably the first two rules are
enforced in some countries, but that varies from country to country; the
accounting laws remain the same.

So now we have a method for distinguishing an accounting law from a business
rule.  How do we translate that from thought to code?


The OpenERP case
================

Let's inspect how does Odoo verifies the accounting law.  Our focus of
attention is the class ``account_move`` (which deals with accounting entries)
in the file ``addons/account/account.py``.  The method that verifies if one or
several entries are correct is the ``validate()`` method.  The method is quite
long, and, as many things in the OpenERP code base, does more than one thing.
It does the following for each journal entry provided [#many-objs]_:

- First it sums all the debits and credits,

- It Checks that all lines touch accounts of the same company.

- It Collects draft lines for further processing.

- If both the account of a line and the line itself explicitly state a
  currency, it checks that either:

  a) they are the same or

  b) the account's is the same as the company's.

  In other words: if the line's currency is not same as the account, then the
  account's currency must be equal to the company's currency.

- The result of the sum all debits minus the sum all credits should be zero
  (actually, less than 0.0001).  This is the accounting law I was looking for.

  So they collect this entry as a valid one.

- If there are any draft lines (collected in the 3rd step), they are marked as
  valid *bypassing any validation*.

  Only in this case as well (I don't know why yet) for lines in a sales or
  purchase journal, ``validate()`` *seems* to try to apply taxes
  [#cuban-taxes]_.  But `I don't see how`__ that code would actually be
  reached.

  Anyway I think this should not be here.

- If the sum of debits minus credits is not (close to) zero, it checks if this
  is a "centralization" journal.  If it is they mark this entry as valid and
  also *update* the entries by centralizing them...  But I won't discuss this.

  Again, it seems that ``validate()`` does at lot besides *validation*.

- If the journal is not a centralizing one and the lines do not obey the
  accounting law, it rejects it... Finally.  Also, it marks all non-draft
  lines as drafts.

- But this is not the end. For each entry that is valid after all, it also
  calls the ``create_analytic_lines`` for the all the lines of valid entries.


__ https://github.com/odoo/odoo/issues/2753


The ``validate()`` method is called when you try to *post* one or more
entries.  It's not called automatically by the ORM when you create an entry.
This is because the entries are allowed to be invalid until they are actually
being recorded as accounting facts (posting them).  Only then they are
required to comply with the accounting laws.

The ``post()`` method creates a unique name for entries that don't have it.
But if the journal where they are being posted into has no sequence
associated, it signals an error.

``post()`` is called by the ``button_validate()`` method.  Which, first,
validates that all the accounts in an entry belong to the same chart of
accounts.

So it seems that validations is both spread and tangled.  It's hard to
differentiate choices from requirements.  A probable concern is performance.
Tangling is one of its effects shown in the `AOP original paper`_.  But even
so, this code shows tangling that is probably too artificial.

For business rules like the ones shown at the beginning of this article, we
have to inspect the ``account_invoice.py`` module of the same addon, and
probably others that modify the ``account.invoice`` object.  But let's focus
on the basics.

Creating journal entries from an invoice is done in the
``action_move_create()`` method.  Again, it's an unwieldy pile of code of 172
lines.  Being a mechanical process of creation I expected to see only data
*translation* from an invoice to a journal entry with lines.  Nevertheless the
code is filled with **validation** checks:

- There should be items in the invoice.

- If you (the user of Odoo) belong to some groups then it'll check the total
  sum of the invoice.  This is actually preceded by a comment that states this
  feature is disabled (but the code remains).

- Payment term calculations are required to match expected amount.

- Checks the type of the journal.

And, yes, it will *also* create an entry with the desired schematic in the
invoice's journal.


Disclaimer
==========

Despite all its flaws, Odoo remains a good solution for many enterprises.
We're using it low and high for everything.

But the source is not friendly because choices are deeply tangled inside the
code.  Methods are ridiculously long.  Which makes them really hard to read,
understand and maintain.


Notes
=====

.. [#double-entry] See `Double-entry bookkeeping`_.

.. [#many-objs] Odoo's models are designed to operate on collections of
   objects instead of a single object.

.. [#cuban-taxes] Here, at Cuba, we don't have much experience with taxes.
   There are no taxes for the common people: No income tax, no IVA
   (VAT)... nothing.  Enterprises do pay some taxes but most people are
   unaware of this fact.

.. _7.0 branch: https://github.com/odoo/odoo/tree/7.0
.. _8.0 branch: https://github.com/odoo/odoo/tree/8.0

.. _Double-entry bookkeeping: http://en.wikipedia.org/wiki/Double-entry_bookkeeping


..
   Local Variables:
   ispell-dictionary: "en"
   End:
