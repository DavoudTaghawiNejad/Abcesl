.. abcESL documentation master file, created by
   sphinx-quickstart on Wed Sep  6 20:33:17 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to abcESL's documentation!
==================================

Introduction
------------

ABCESL is an accounting and contracting framework for ABCE. It was originally developed by
Rafa Babtista, Alissa Kleinnijenhuis and Thom Wetzer and subsequently distilled and refined by
Rudy Tanin, Davoud Taghawi-Nejad. Originally it was conceived as a framework to run
systemic stress testing exercises for the financial sector.
Currently it is used in the resilience project as well as in an insurance modeling
project.

In order to install abcesl, first install ABCE (abce.readthedocs.io) and then
install :code:`sudo python3 -m pip install abcesl` or
:code:`sudo pypy3 -m pip install abcesl`.

You can than create agents that inherit from abcesl.Agent instead of abce.Agent.
Like abce agents these agents have an inventory of goods :code:`self['cookies']`,
but they also have an inventory of contracts and set of accounts that book the
values of goods and contracts.

ABCESL is part of the wider effort of the Economic Simulation Library at
the Institute for New Economic Thinking at Oxford University.


.. toctree::
   :maxdepth: 2
   :caption: Contents:


   agent
   ledger
   account
   contract
   contracting
   obligations
   obligationmessage
   exception


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
