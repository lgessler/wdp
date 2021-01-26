# -*- coding: utf-8 -*-
"""
TODO
"""
import logging
import os
import pickle
from pprint import pformat
from zipfile import ZipFile
from typing import List

_logger = logging.getLogger(__name__)


class _DefaultReprMixin:
    """Internal mixin class that provides a __repr__ implementation that shows all non-callable attrs"""

    def __repr__(self):
        class_name = self.__class__.__name__
        data_string = ", ".join(
            str(k) + "=" + ('"' + v + '"' if isinstance(v, str) else str(v))
            for k, v in self.__dict__.items()
            if not callable(v)
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


class AlternateForm(_DefaultReprMixin, _ToDictMixin):
    def __init__(self, alternate_form: str, description_of_use: str = None):
        self.alternate_form = alternate_form
        self.description_of_use = description_of_use


class Pronunciation(_DefaultReprMixin, _ToDictMixin):
    def __init__(self, pronunciation: str, notation: str = None):
        self.pronunciation = pronunciation
        self.notation = notation


class Definition(_DefaultReprMixin, _ToDictMixin):
    def __init__(self, definition: str, part_of_speech: str):
        self.definition = definition
        self.part_of_speech = part_of_speech.capitalize()


class Word(_DefaultReprMixin, _ToDictMixin):
    """
    TODO
    """

    def __init__(self, word_form):
        self.word_form = word_form
        self.definitions = []
        self.alternate_forms = []
        self.pronunciations = []
        self.etymology = None
        self.description = None
        self.references = None
        self.usage_notes = None

    def add_definition(self, definition: str, part_of_speech: str):
        self.definitions.append(Definition(definition, part_of_speech))

    def add_alternate_form(self, alternate_form: str, description_of_use: str = None):
        self.alternate_forms.append(AlternateForm(alternate_form, description_of_use=description_of_use))

    def add_pronunciation(self, pronunciation: str, notation: str = None):
        self.pronunciations.append(Pronunciation(pronunciation, notation=notation))

    def set_etymology(self, etymology: str):
        self.etymology = etymology

    def set_description(self, description: str):
        self.description = description

    def set_references(self, references: str):
        self.references = references

    def set_usage_notes(self, usage_notes: str):
        self.usage_notes = usage_notes


def export_words(words: List[Word], filepath: str):
    if filepath[-4:] != ".zip":
        filepath += ".zip"
    f = ZipFile(filepath, 'w')
    f.writestr('words.pkl', pickle.dumps(words))
    f.close()
    _logger.info(f"Wrote words to {filepath}")


def import_words(filepath: str) -> List[Word]:
    if not os.path.isfile(filepath):
        raise Exception(f"File '{filepath}' does not exist.")
    f = ZipFile(filepath, 'r')
    words = pickle.loads(f.read('words.pkl'))
    f.close()
    return words
