======================================================
 Business rules: A case about coding standards/issues
======================================================


.. categories:: OpenERP, Odoo
.. tags:: integration, programming

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


The accountant that told you that, was generous enough not to use the
`T-account`__ representation, but she made several assumptions:

a) There is a single or definite "Sales" journal.

b) There is a single or definite "Receivable" account.

c) There is a single or definite "Sales" account.

__ http://en.wikipedia.org/wiki/Debits_and_credits#T-accounts

Then she will tell you that:

   Whenever you receive payment for an invoice you must create an entry in the
   "Bank" journal with the following two items (schematic):

::

   Accounts          | Debits            |   Credits
   ------------------+-------------------+-------------------
   Receivable        |                   |  $ XXXX
   ------------------+-------------------+-------------------
            Bank     | $ XXXX            |
   ------------------+-------------------+-------------------

She will probably explain that this entry somehow "cancels" the previous one,
so that now you know you should not must receive any further payment for those
"$ XXXX" you were entitled to collect.

Compare those rules with the following:

  For a single (journal) entry to be valid, the sum of the debits of all its
  items must be equal to the sum the credits of all its items.

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

Let's inspect how does OpenERP [#not-odoo]_ verifies the accounting law.  Our
focus of attention is the class ``account_move`` (which deals with accounting
entries) in the file ``addons/account/account.py``.  The method that verifies
if one or several entries are correct is the ``validate()`` method.  The
method is quite long, and, as many things in the OpenERP code base, does more
than one thing.  It does the following for each journal entry provided
[#many-objs]_:

- First the sum all the debits and credits

- Check that all lines touch accounts of the same company.

  .. note:: The ``post()`` method will see later checks that all accounts
     belong to the same Chart of Accounts.

- Collect draft lines for further processing.

- If both the account of a line and the line itself explicitly state a
  currency, check that either:

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
  [#cuban-taxes]_.  But I don't see how that code would actually be reached.
  In the appendix__ this is lines 45-62.

  Anyway I think this should not be here.

- If the sum of debits minus credits is not (close to) zero, it checks if this
  is a "centralization" journal.  If it is they mark this entry as valid and
  also *update* the entries by centralizing them...  But I won't discuss this.

  Again, it seems that ``validate()`` does at lot besides *validate*.

- If the journal is not a centralizing one and the lines do not obey the
  accounting law, it rejects it... Finally.  Also, it marks all non-draft
  lines as drafts.

- But this is not the end. For each entry that is valid after all, it also
  calls the ``create_analytic_lines`` for the all the lines of valid entries.

  Why?

__ `Appendix - The validate() method as of OpenERP 7.0, the 19th Sep, 2014`_


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
Tangling is one of its effects as shown in the `AOP original paper`_.  But
even so, this code shows tangling that is probably too artificial.

For business rules like the ones shown at the beginning of this article, we
have to inspect the ``account_invoice.py`` module of the same addon, and
probably others that modify the ``account.invoice`` object.  But let's focus
on the basics.

Creating journal entries from an invoice is done in the
``action_move_create()`` method.  Again, it's an unwieldy pile of code of 160
lines.  Being a mechanical process of creation I expected to see only data
*translation* from an invoice to a journal entry with lines.  Nevertheless the
code is filled with **validation** checks:

- There should be items in the invoice.

- If you (the user of OpenERP) belong to some groups then it'll check the
  total sum of the invoice.

- Payment term calculations are required to match expected amount.

- Checks the type of the journal.

And, yes, it will *also* create an entry with the desired schematic in the
invoice's journal.


Disclaimer
==========

Despite all its flaws, OpenERP remains a good solution for many enterprises.
We're using it low and high for everything.

But the source is not friendly because choices are deeply tangled inside the
code.  Methods are ridiculously long.  Which makes them really hard to read,
understand and maintain.


Notes
=====

.. [#double-entry] See `Double-entry bookkeeping`_.

.. [#not-odoo] While I'm writing these lines OpenERP is a moving target and
   the branch I'm currently concerned with is the `7.0 branch`_.  Things are
   changing in the `8.0 branch`_ in ways I'm not entirely familiar with yet.

.. [#many-objs] OpenERP's models are designed to operate on collections of
   objects instead of a single object.

.. [#cuban-taxes] Here, at Cuba, we don't have much experience with taxes.
   There are no taxes for the common people: No income tax, no IVA
   (VAT)... nothing.  Enterprises do pay some taxes but most people are
   unaware of this fact.

.. _7.0 branch: https://github.com/odoo/odoo/tree/7.0
.. _8.0 branch: https://github.com/odoo/odoo/tree/8.0

.. _Double-entry bookkeeping: http://en.wikipedia.org/wiki/Double-entry_bookkeeping


Appendix - The ``validate()`` method as of OpenERP 7.0, the 19th Sep, 2014
==========================================================================

.. code-block:: python
   :linenos:

   def validate(self, cr, uid, ids, context=None):
       if context and ('__last_update' in context):
	   del context['__last_update']

       valid_moves = [] #Maintains a list of moves which can be responsible to create analytic entries
       obj_analytic_line = self.pool.get('account.analytic.line')
       obj_move_line = self.pool.get('account.move.line')
       for move in self.browse(cr, uid, ids, context):
	   journal = move.journal_id
	   amount = 0
	   line_ids = []
	   line_draft_ids = []
	   company_id = None
	   for line in move.line_id:
	       amount += line.debit - line.credit
	       line_ids.append(line.id)
	       if line.state=='draft':
		   line_draft_ids.append(line.id)

	       if not company_id:
		   company_id = line.account_id.company_id.id
	       if not company_id == line.account_id.company_id.id:
		   raise osv.except_osv(_('Error!'), _("Cannot create moves for different companies."))

	       if line.account_id.currency_id and line.currency_id:
		   if line.account_id.currency_id.id != line.currency_id.id and (line.account_id.currency_id.id != line.account_id.company_id.currency_id.id):
		       raise osv.except_osv(_('Error!'), _("""Cannot create move with currency different from ..""") % (line.account_id.code, line.account_id.name))

	   if abs(amount) < 10 ** -4:
	       # If the move is balanced
	       # Add to the list of valid moves
	       # (analytic lines will be created later for valid moves)
	       valid_moves.append(move)

	       # Check whether the move lines are confirmed

	       if not line_draft_ids:
		   continue
	       # Update the move lines (set them as valid)

	       obj_move_line.write(cr, uid, line_draft_ids, {
		   'state': 'valid'
	       }, context, check=False)

	       account = {}
	       account2 = {}

	       if journal.type in ('purchase','sale'):
		   for line in move.line_id:
		       code = amount = 0
		       key = (line.account_id.id, line.tax_code_id.id)
		       if key in account2:
			   code = account2[key][0]
			   amount = account2[key][1] * (line.debit + line.credit)
		       elif line.account_id.id in account:
			   code = account[line.account_id.id][0]
			   amount = account[line.account_id.id][1] * (line.debit + line.credit)
		       if (code or amount) and not (line.tax_code_id or line.tax_amount):
			   obj_move_line.write(cr, uid, [line.id], {
			       'tax_code_id': code,
			       'tax_amount': amount
			   }, context, check=False)
	   elif journal.centralisation:
	       # If the move is not balanced, it must be centralised...

	       # Add to the list of valid moves
	       # (analytic lines will be created later for valid moves)
	       valid_moves.append(move)

	       #
	       # Update the move lines (set them as valid)
	       #
	       self._centralise(cr, uid, move, 'debit', context=context)
	       self._centralise(cr, uid, move, 'credit', context=context)
	       obj_move_line.write(cr, uid, line_draft_ids, {
		   'state': 'valid'
	       }, context, check=False)
	   else:
	       # We can't validate it (it's unbalanced)
	       # Setting the lines as draft
	       not_draft_line_ids = list(set(line_ids) - set(line_draft_ids))
	       if not_draft_line_ids:
		   obj_move_line.write(cr, uid, not_draft_line_ids, {
		       'state': 'draft'
		   }, context, check=False)
       # Create analytic lines for the valid moves
       for record in valid_moves:
	   obj_move_line.create_analytic_lines(cr, uid, [line.id for line in record.line_id], context)

       valid_moves = [move.id for move in valid_moves]
       return len(valid_moves) > 0 and valid_moves or False

..
   Local Variables:
   ispell-dictionary: "en"
   End:
