================
 Business rules
================

.. categories:: OpenERP, Odoo
.. tags:: integration

How do you express a business rule in your code?  Would recognize it a
separate thing that you may or may not use?  For instance, how would you
encode the following rule:

   Whenever you send a customer an invoice for something you have shipped to
   him/her, you must create an entry in the "Sales" Journal with the following
   two items (schematic):

::

   Accounts          | Debits            |   Credits
   ------------------+-------------------+-------------------
   Account           |                   |
   receivable        | $ XXXX            |
   ------------------+-------------------+-------------------
            Sales    |                   |  $ XXXX
   ------------------+-------------------+-------------------


The accountant that told you that was generous enough not to use the T-account
representation, but she made several assumptions:

a) There is a single or definite "Sales" journal.

b) There is a single or definite "Account receivable".

c) There is a single or definite "Sales" account.

She will then tell you that

   Whenever you receive payment for an invoice you must create an entry in the
   "Bank" journal with the following two items (schematic):

::

   Accounts          | Debits            |   Credits
   ------------------+-------------------+-------------------
   Account           |                   |
   receivable        |                   |  $ XXXX
   ------------------+-------------------+-------------------
            Bank     | $ XXXX            |
   ------------------+-------------------+-------------------

She will probably explain that this entry somehow "cancels" the previous one,
so that now you know you should not must receive any further payment for those
"$ XXXX".  Of course, you will ask many questions:

- What about if you need the cash before the shipping.

- What about if you need an advance and then the rest.

And many others.  But I want you to focus on those two rules, cause the rules
derived from the other cases will do the same for the argument I'm about to
raise.

Compare those rules with the following:

  For a single (journal) entry to be valid, the sum of the debits of all its
  items must be equal to the sum the credits of all its items.

Is this the same kind of rule?  Obviously not.  The first ones state how you
should generate an entry in the face of a business case.  The last one which
entries are valid no matter what they should record.  In fact, the first two
rules must ensure they generate entries that comply with this restriction.  So
I won't call this last one a rule anymore, it's kind of an accounting law.
Yes, probably the first two rules are enforced in some countries, but that
varies from country to country; the accounting laws remain the same.

So now we have a method for distinguishing an accounting law from a business
rule.  How do we translate that from thought to code?

The OpenERP case
================

Let's inspect how does OpenERP verifies the law.  Our focus of attention is
the class ``account_move`` (which deals with accounting entries) in the file
``addons/account/account.py``.  The method that verifies if one or several
entries are correct is the ``validate()`` method.


..
   Local Variables:
   ispell-dictionary: "en"
   End:
