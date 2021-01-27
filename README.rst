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

.. contents:: Contents

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
As in the example above, you will need to build a list of :code:`Word` objects. A single
:code:`Word` object is defined by its canonical form. It is OK for two or more words to
have the same form--this might happen when two words are homonyms, or when they have
separate etymologies.

.. code-block:: python

    from wdp import Word
    bank_1 = Word("bank")
    bank_1.add_definition("A place where people keep their money", "Noun")

    bank_2 = Word("bank")
    bank_2.add_definition("The edges of a river", "Noun")

Methods of the :code:`Word` class which begin with :code:`add_` can be invoked multiple
times (because e.g. a word can have many definitions), but methods which begin with
:code:`set_` should only be called once (because e.g. you should only have one
etymological note).

Consult the `Word class's documentation`_ for a complete description of its methods.
Currently, the following methods are available:

- add_definition
- add_alternative_form
- add_pronunciation
- set_etymology
- set_description
- set_references
- set_usage_notes
- set_conjugation
- set_declension
- set_inflection

For more information on how to use these methods, see Wiktionary's
`entry layout guidelines`_.

.. _Word class's documentation: http://lgessler.com/wdp/api/wdp.html#wdp.models.Word
.. _entry layout guidelines: https://en.wiktionary.org/wiki/Wiktionary:Entry_layout

Step 2, option 1 (Recommended): Export :code:`Word` Objects
-----------------------------------------------------------

Once you have constructed your list of words, they are ready to be uploaded.
Uploading to Wiktionary is a bit complicated, so we recommend that you export
your data so someone else can upload it. You can do this by using the
:code:`export_words` function:

.. code-block:: python

    from wdp import export_words
    my_english_words = [bank_1, bank_2]
    export_words(my_english_words, 'my_english_words.zip')

Once you've done this, please email it to Luke Gessler (lg876@georgetown.edu)
or Aryaman Arora (aa2190@georgetown.edu) so we can help you perform your upload.

Step 2, option 2 (Advanced): Format and Upload :code:`Word` Objects
-------------------------------------------------------------------

*Section under construction*

First, you will need to `create an account on Wiktionary`_.

.. _create an account on Wiktionary: https://en.wiktionary.org/w/index.php?title=Special:CreateAccount&returnto=Wiktionary%3AMain+Page

Next, in your working directory, create a :code:`user-config.py` file with
the following contents:

.. code-block:: python

    family = "wiktionary"
    mylang = "en"

    usernames["wiktionary"]["en"] = u"Ldgessler"  # change to your username

    console_encoding = "utf-8"

    minthrottle = 0
    maxthrottle = 1

In your main Python file, you can now use :code:`wdp.upload.upload_formatted_entries`
to perform your upload:

.. code-block:: python

    # load your list of Words
    from wdp.upload import upload_formatted_entries
    my_english_words = [...]
    # or
    from wdp import import_words
    my_english_words = import_words('my_english_words.zip')

    # format the list of Words into entries
    # you will need a language code from here:
    # https://en.wiktionary.org/wiki/Wiktionary:List_of_languages
    from wdp import format_entries
    lang_code = "en"
    lang_name = "English"
    formatted_entries = format_entries(my_english_words, lang_code, lang_name)

    # use the page_prefix argument to upload the data to your personal pages
    # first for debugging, e.g. User:Ldgessler/chafe
    upload_formatted_entries(formatted_entries, lang_name, page_prefix="User:Ldgessler/")

    # Once you are CERTAIN your data is correct, you may remove the page_prefix
    # argument to perform the upload for real:
    upload_formatted_entries(formatted_entries, lang_name)

FAQ
===

I don't know Python. Can I still use WDP?
-----------------------------------------
Not on your own, but please `open an issue`_ on our GitHub page explaining what your data looks like, and
someone may be available to help you.

.. _open an issue: https://github.com/lgessler/wdp/issues/new

I have data in *X* format. Will WDP work with it?
-------------------------------------------------
Yes, WDP is agnostic as to the source format of your data.

In the future, we may add support for popular formats (like `FLEx dictionary XML`_) to allow you to upload from them
without writing any code. If there is a format you'd like us to support, please `open an issue`_.

.. _FLEx dictionary XML: https://software.sil.org/fieldworks/wp-content/uploads/sites/38/2018/03/Export-options-in-Flex.pdf

What should I do if my language doesn't have a code?
----------------------------------------------------
Contact Aryaman Arora (aa2190@georgetown.edu) or a Wiktionary admin.

