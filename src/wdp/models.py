# -*- coding: utf-8 -*-
"""
TODO
"""
import logging
import pywikibot, re

from wdp import __version__

__author__ = "Luke Gessler"
__copyright__ = "Luke Gessler"
__license__ = "mit"

_logger = logging.getLogger(__name__)

POS_SHORTCUTS = {
    'n': 'noun',
    'v': 'verb',
    'adj': 'adjective',
    'prep': 'preposition',
    'adv': 'adverb'
}


class _DefaultReprMixin:
    """Internal mixin class that provides a __repr__ implementation that shows all non-callable attrs"""
    def __repr__(self):
        class_name = self.__class__.__name__
        data_string = ", ".join(str(k) + "=" + ('"' + v + '"' if isinstance(v, str) else str(v))
                                for k, v in self.__dict__.items()
                                if not callable(v))
        return f'{class_name}({data_string})'


class AlternateForm(_DefaultReprMixin):
    def __init__(self, alternate_form, description_of_use=None):
        self.alternate_form = alternate_form
        self.description_of_use = description_of_use


class Pronunciation(_DefaultReprMixin):
    def __init__(self, pronunciation, notation=None):
        self.pronunciation = pronunciation
        self.notation = notation


class Definition(_DefaultReprMixin):
    def __init__(self, definition, part_of_speech=None):
        if isinstance(definition, str):
            definition = [definition]
        self.definition = definition
        self.part_of_speech = part_of_speech


class Entry(_DefaultReprMixin):
    """
    TODO
    """
    def __init__(self,
                 word_form, lang_code, lang_name):
        self.word_form = word_form
        self.lang_code = lang_code
        self.lang_name = lang_name
        self.definitions = []
        self.alternate_forms = []
        self.pronunciations = []

    def add_definition(self, definition, part_of_speech=None):
        self.definitions.append(
            Definition(definition, part_of_speech=part_of_speech)
        )

    def add_alternate_form(self, alternate_form, description_of_use=None):
        self.alternate_forms.append(
            AlternateForm(alternate_form, description_of_use=description_of_use)
        )

    def add_pronunciation(self, pronunciation, notation=None):
        self.pronunciations.append(
            Pronunciation(pronunciation, notation=notation)
        )

    def export(self):
        result = f'=={self.lang_name}=='

        if self.alternate_forms:
            result += '\n\n===Alternative forms===\n'
            result += '\n'.join([f'* {{{{alter|{self.lang_code}|{x.alternate_form}||{x.description_of_use}}}}}' for x in self.alternate_forms])

        if self.pronunciations:
            result += '\n\n===Pronunciation===\n* {{IPA|' + self.lang_code + '|'
            result += '|'.join([x.pronunciation for x in self.pronunciations])
            result += '}}'

        if self.definitions:
            for definition in self.definitions:
                part_of_speech = POS_SHORTCUTS.get(definition.part_of_speech, definition.part_of_speech)
                if part_of_speech == None:
                    raise Exception("A part of speech is required.")
                result += f'\n\n==={part_of_speech.capitalize()}==='
                result += f'\n{{{{head|{self.lang_code}|{part_of_speech}}}}}\n'
                for sense in definition.definition:
                    result += f'\n# {sense}'
        else:
            raise Exception("The entry has no definitions. At least one definition is required.")
        
        return result

    def upload(self):
        site = pywikibot.Site(code='en', fam='wiktionary')
        site.login()

        page = pywikibot.Page(site, self.word_form)
        order = re.findall(r'(^|\n)==([^=]*?)==[\n]', page.text)
        print(page.text)
        print(order)
        
        if order:
            for _, lang in order:
                if lang == self.lang_name:
                    print(f'Entry already exists for {self.lang_name} at "{self.word_form}", skipping.')
                    return
                elif lang > self.lang_name:
                    page.text = page.text.replace(f'=={lang}==', f'{self.export()}\n\n----\n\n=={lang}==')
                    break
        else:
            page.text = self.export()

        page.save(f'Automatic import of {self.lang_name} entry with WDP.')


