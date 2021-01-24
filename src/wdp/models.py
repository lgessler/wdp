# -*- coding: utf-8 -*-
"""
TODO
"""
import logging

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
        d = {}
        for k, v in self.__dict__.items():
            if callable(v):
                continue
            elif isinstance(v, list) or isinstance(v, tuple):
                d[k] = [v2 if not hasattr(v2, "to_dict") else v2.to_dict() for v2 in v]
            else:
                d[k] = v if not hasattr(v, "to_dict") else v.to_dict()

        return d


class AlternateForm(_DefaultReprMixin, _ToDictMixin):
    def __init__(self, alternate_form, description_of_use=None):
        self.alternate_form = alternate_form
        self.description_of_use = description_of_use


class Pronunciation(_DefaultReprMixin, _ToDictMixin):
    def __init__(self, pronunciation, notation=None):
        self.pronunciation = pronunciation
        self.notation = notation


class Definition(_DefaultReprMixin, _ToDictMixin):
    def __init__(self, definition, part_of_speech=None):
        self.definition = definition
        self.part_of_speech = part_of_speech


class Word(_DefaultReprMixin, _ToDictMixin):
    """
    TODO
    """

    def __init__(self, word_form):
        self.word_form = word_form
        self.definitions = []
        self.alternate_forms = []
        self.pronunciations = []

    def add_definition(self, definition, part_of_speech=None):
        self.definitions.append(Definition(definition, part_of_speech=part_of_speech))

    def add_alternate_form(self, alternate_form, description_of_use=None):
        self.alternate_forms.append(AlternateForm(alternate_form, description_of_use=description_of_use))

    def add_pronunciation(self, pronunciation, notation=None):
        self.pronunciations.append(Pronunciation(pronunciation, notation=notation))
