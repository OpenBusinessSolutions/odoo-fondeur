.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================
Stock Picking Invoicing Unified
===============================

Odoo allows to select several pickings and click on "Create Draft Invoices"
option for creating the corresponding invoice(s) depending if you have
selected several partners and if you have marked the "Group by partner"
check.

But it only takes into account the first picking for selecting the type of the
invoice you are going to create (customer/supplier invoice/refund), mixing all
the lines on it. And not only that: if you have returned pickings, the returned
quantities are summed to the rest, instead of decreasing the amount to invoice,
which is the common practise when you have some returns.

This module overpasses this limitation, allowing to invoice them all together
without having to worry about that, and also having the extra feature of
reducing the amount in the invoice when you have delivered or received goods
and some of them (or previous ones) have been returned, instead of needing
to create 2 invoices and to conciliate them for the final/real amount.

Usage
=====

* Select several pickings from any of the menus that allows it (
  *Warehouse > All Operations* and click on any of the lines,
  *Purchases > Invoice Control > On Incoming Shipments*, etc).
* Click on *More > Create Draft Invoices*.
* In the resulting dialog, the proper invoices types that are going to be
  created are computed, and you have to select the journals for that types.
* Click on *Create* button, and the invoices will be correctly created.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/188/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/odoomrp/odoomrp-wip/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/odoomrp/odoomrp-wip/issues/new?body=module:%20
stock_picking_invoicing_unified%0Aversion:%20
8.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------
* Ainara Galdona <ainaragaldona@avanzosc.es>
* Pedro M. Baeza <pedro.baeza@serviciobaeza.com>
