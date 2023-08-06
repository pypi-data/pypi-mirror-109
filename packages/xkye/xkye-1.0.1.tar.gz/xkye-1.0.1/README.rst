.. _Pypi Readme File:

====================
Xkye Python Library
====================

Introducing `Xkye-Python <https://github.com/RahmanAnsari/xkye_python>`_ standard library to provide objective query builder for `xkye <https://github.com/RahmanAnsari/xkye-lang>`_ language. You can easily query the entities from the xkye file using this library. It provides a more convenient and idiomatic way to write and manipulate queries.

|

Installation
=============
Install library with pypi:

.. code-block:: bash

  $ pip3 install xkye

|

Usage
======

.. code-block:: bash
  
  from xkye import IO as io

  #initiate the xkye with io
  x = io(filename.xky)

  #read the contents of the file
  x.read()

  #get the output of any of the entity from teh xky file
  #to get the value of the entity
  x.get("entityname")

  #to get the value of the entity in the given clutch
  x.get("entityname","clutchname")

  #to get the value of the entity in the given cluth's span
  x.get("entityname","clutchname", clutchspan)

  #to get the span count of the given cluster
  x.getSpan("clustername")

|

Examples
=========

Please use the `examples <https://github.com/RahmanAnsari/xkye_python/tree/main/examples>`_ directory to see some complex examples using xkye-pyhton library. For details about xkye syntax and format, use the offical `Xkye-lang <https://github.com/RahmanAnsari/xkye-lang>`_ documentation.

|

Documentation
==============

Documentation is available at `<xkye-python.readthedocs.io>`_ .

|

Version matrix
===============

.. list-table::
   :header-rows: 1

   * - Xkye version
     - Xkye-Python Library version
   * - >= 1.0.0
     - >= 1.0.0

|

Upcoming features on or before v2.0.0
========================================
* Ability to get the span limit of the given cluster (Completed)
* Ability to add entity, clutch and subclutch

|

Contribution Guide
====================

Want to hack on Xkye-Python? Awesome! We have `Contribution-Guide <https://github.com/RahmanAnsari/xkye_python/blob/main/CONTRIBUTING.md>`_ on our official repo. If you are not familiar with making a pull request using GitHub and/or git, please read `this guide <https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests>`_ . If you're looking for ways to contribute, please look at our `issue tracker <https://github.com/RahmanAnsari/xkye_python/issues>`_ .

|

License
=========
Xkye-python is open-source standard python library for xkye language that is released under the MIT License. For details on the license, see the `LICENSE <https://github.com/RahmanAnsari/xkye_python/blob/main/LICENSE>`_ file.

|

If you like this library, help me to develop it by buying a cup of coffee

|buy me a coffee|

.. |buy me a coffee| image:: https://cdn.buymeacoffee.com/buttons/default-orange.png 
   :target: https://www.buymeacoffee.com/rahmanansari
   :width: 174
   :alt: Buy Me A Coffee Badge
   :height: 41
