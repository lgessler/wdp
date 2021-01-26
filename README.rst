=================================
wdp: the Wiktionary Data Preparer
=================================

Introduction
============

**wdp (Wiktionary Data Preparer)** is a small Python library that can help you get your language
data onto Wiktionary. Formatting Wiktionary entries perfectly can be hard, and it's wdp's goal
to take care of the tricky stuff for you.

Example
-------

.. code-block:: python

    from wdp import Word, format_entries, export_words

    # use the Word class to represent our words
    apple = Word("apple")
    apple.add_pronunciation("/ˈæp.əl/", notation="IPA")
    apple.add_definition("A common, round fruit", "Noun")
    apple.add_definition("A tree of the genus Malus", "Noun")
    apple.set_etymology("Old English æppel < Proto-Germanic *ap(a)laz < PIE *ab(e)l-")

    pear = Word("pear")
    # ...

    # put all our words in a list
    wdp_words = [apple, pear, ...]

    # Generate Wiktionary markup from our entries
    formatted_entries = format_entries(wdp_words, "en", "English")
    # Wikitext markup for "apple":
    # ('==English==\n'
    #  '===Etymology===\n'
    #  'Old English æppel < Proto-Germanic *ap(a)laz < PIE *ab(e)l-\n'
    #  '\n'
    #  '===Noun===\n'
    #  '{{head|en|Noun}}\n'
    #  '# A common, round fruit\n'
    #  '# A tree of the genus Malus\n'
    #  '\n')
    #


    # Perform the upload
    from wdp.upload import upload_formatted_entries
    upload_formatted_entries(formatted_entries, "English")

Installation
============

(Note: wdp requires **Python 3.6 or higher**. If you do not have a Python installation, we
recommend that you use `Anaconda`_.)

.. _Anaconda: https://www.anaconda.com/products/individual#Downloads
.. code-block:: bash

    pip install wdp

Usage
=====

Prerequisites
-------------

To use wdp, you will need to have your data available in a machine-readable format. The
format does not matter, but you will need to be able to read it and turn it into a list
of :code:`Word` objects.

Step 1: Build :code:`Word` Objects
----------------------------------


Step 2, option 1 (Recommended): Export :code:`Word` Objects
-----------------------------------------------------------

Step 2, option 2 (Advanced): Format and Upload :code:`Word` Objects
-------------------------------------------------------------------

FAQ
===

TODO