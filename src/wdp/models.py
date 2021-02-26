# -*- coding: utf-8 -*-
"""
TODO
"""
import logging
import os
import pickle
from pprint import pformat
from zipfile import ZipFile
from typing import List, Tuple, Iterable

_logger = logging.getLogger(__name__)


class _DefaultReprMixin:
    """Internal mixin class that provides a __repr__ implementation that shows all non-callable attrs"""

    def __repr__(self):
        class_name = self.__class__.__name__
        data_string = ", ".join(
            str(k) + "=" + ('"' + v + '"' if isinstance(v, str) else str(v))
            for k, v in self.__dict__.items()
            if not callable(v) and v is not None
        )
        return f"{class_name}({data_string})"


class _ToDictMixin:
    def to_dict(self):
        """Return all non-callable attributes in this Entry object as a dictionary recursively"""
        d = {'__class__': self.__class__.__name__}
        for k, v in self.__dict__.items():
            if callable(v):
                continue
            elif isinstance(v, list) or isinstance(v, tuple):
                d[k] = [v2 if not hasattr(v2, "to_dict") else v2.to_dict() for v2 in v]
            else:
                d[k] = v if not hasattr(v, "to_dict") else v.to_dict()

        return d

    def pretty_format(self):
        return pformat(self.to_dict())


class AlternativeForm(_DefaultReprMixin, _ToDictMixin):
    def __init__(self, alternative_form: str, description_of_use: str = None):
        self.alternative_form = alternative_form
        self.description_of_use = description_of_use


class Pronunciation(_DefaultReprMixin, _ToDictMixin):
    def __init__(self, pronunciation: str, notation: str = None):
        self.pronunciation = pronunciation
        self.notation = notation


class Definition(_DefaultReprMixin, _ToDictMixin):
    def __init__(self, definition: str, part_of_speech: str, usage_examples: list = None):
        self.definition = definition
        self.part_of_speech = part_of_speech.capitalize()
        self.usage_examples = usage_examples or []


class UsageExample(_DefaultReprMixin, _ToDictMixin):
    def __init__(self, text: str, translation: str):
        self.text = text
        self.translation = translation


class Word(_DefaultReprMixin, _ToDictMixin):
    """
    An object that represents a single "word". If two or more Word objects have the same
    word_form attribute, their information will appear under separate headings "Etymology 1",
    "Etymology 2", etc. (see for instance: https://en.wiktionary.org/wiki/graft#English).

    Information is added to the object by using the methods beginning with `add_` and `set_`.
    String arguments of these methods may contain wikitext markup in case you want to use it to
    e.g. link to other entries using the [[square bracket]] notation. For more information, see:
    https://en.wikipedia.org/wiki/Help:Wikitext


    """

    def __init__(self, word_form):
        """
        Initialize a Word object. `word_form` will be used to determine the URL of this word's
        entry on Wiktionary: for example, a Word object with word_form "graft" in English would
        appear at "https://en.wiktionary.org/wiki/graft".

        Args:
            word_form: A canonical orthographic representation of a word.
        """
        self.word_form = word_form
        self.definitions = []
        self.alternative_forms = []
        self.pronunciations = []
        self.etymology = None
        self.description = None
        self.references = None
        self.usage_notes = None
        self.declension = None
        self.conjugation = None
        self.inflection = None

    def add_definition(self, definition: str, part_of_speech: str, usage_examples: Iterable[Tuple[str, str]] = None):
        """
        Add a definition of this word. A valid part of speech or other lexical categorization is required.
        Part of speech should come from a list of approved parts of speech on Wiktionary if possible:
        https://en.wiktionary.org/wiki/Wiktionary:Entry_layout#Part_of_speech
        Args:
            definition: Freetext explaining one meaning of the word.
            part_of_speech: a lexical categorization of the word that this definition occurs with
            usage_examples: a list of pairs of strings, where the first is the example, and the second is its translation
        """
        self.definitions.append(
            Definition(
                definition,
                part_of_speech,
                [UsageExample(ex, tr) for ex, tr in usage_examples] if usage_examples is not None else None
            )
        )

    def add_alternative_form(self, alternative_form: str, description_of_use: str = None):
        """
        Add an alternative representation of this word in case there are e.g. variant spellings or
        different orthographies. This is NOT for IPA or other kinds of pronunciation guides--
        use `add_pronunciation` for that instead.
        Args:
            alternative_form: a string with the alternative representation of the word
            description_of_use: e.g. "Chiefly British", "Romaji", "Cyrillic"
        """
        self.alternative_forms.append(AlternativeForm(alternative_form, description_of_use=description_of_use))

    def add_pronunciation(self, pronunciation: str, notation: str = None):
        """
        Add a representation of the word that indicates its pronunciation. For IPA, you MUST surround
        it with either [square brackets] or /forward slashes/ to indicate whether it is phonemic or
        phonetic and you MUST set notation to "IPA"
        Args:
            pronunciation: a string that represents the word's pronunciation
            notation: a short description of the notation the pronunciation is given in. Use "IPA" if in IPA.
        """
        self.pronunciations.append(Pronunciation(pronunciation, notation=notation))

    def set_etymology(self, etymology: str):
        """
        Provide an etymological note for the word.
        Args:
            etymology: Freetext explaining the word's etymology.
        """
        self.etymology = etymology

    def set_description(self, description: str):
        """
        Provide a description for the word. Used mostly for symbols. See: 
        https://en.wiktionary.org/wiki/Wiktionary:Entry_layout#Description
        Args:
            description: Freetext describing the word.
        """
        self.description = description

    def set_references(self, references: str):
        """
        Provide references for the information in this Word.
        Args:
            references: Freetext containing references.
        """
        self.references = references

    def set_usage_notes(self, usage_notes: str):
        """
        Provide notes on how the word is used with respect to e.g. formality and other social dimensions.
        Args:
            usage_notes: Freetext containing a usage note.
        """
        self.usage_notes = usage_notes

    def set_declension(self, declension: str):
        """
        Provide declensional information for the word. Only use this for nouns--see `set_conjugation`
        for verbs and `set_inflection` for all other lexical classes.
        Args:
            declension: Freetext describing the noun's declension.
        """
        self.declension = declension

    def set_conjugation(self, conjugation: str):
        """
        Provide conjugational information for the word. Only use this for verbs--see `set_declension`
        for nouns and `set_inflection` for all other lexical classes.
        Args:
            conjugation: Freetext describing the verb's conjugation.
        """
        self.conjugation = conjugation

    def set_inflection(self, inflection: str):
        """
        Provide inflecitonal information for the word. Only use this if the word is not a noun or a verb.
        For nouns, see `set_declension`, and for verbs, see `set_inflection`.
        Args:
            inflection: Freetext describing the word's inflection.
        """
        self.inflection = inflection


def export_words(words: List[Word], filepath: str):
    """
    Export a list of words to a .zip file for sharing with someone who can upload the data to Wiktionary.
    Args:
        words: A list of `Word` objects that have had their information filled out.
        filepath: A location to write the export .zip file to.
    """
    if filepath[-4:] != ".zip":
        filepath += ".zip"
    f = ZipFile(filepath, 'w')
    f.writestr('words.pkl', pickle.dumps(words))
    f.close()
    _logger.info(f"Wrote words to {filepath}")


def import_words(filepath: str) -> List[Word]:
    """
    Read a list of `Word` objects from a file produced by `export_words`.
    Args:
        filepath: Location of the zip
    """
    if not os.path.isfile(filepath):
        raise Exception(f"File '{filepath}' does not exist.")
    f = ZipFile(filepath, 'r')
    words = pickle.loads(f.read('words.pkl'))
    f.close()
    return words
