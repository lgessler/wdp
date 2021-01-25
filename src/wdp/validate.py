# -*- coding: utf-8 -*-
import logging
from typing import List

from wdp import Word

_logger = logging.getLogger(__name__)

VALID_POS = [
    "Adjective",
    "Adverb",
    "Ambiposition",
    "Article",
    "Circumposition",
    "Classifier",
    "Conjunction",
    "Contraction",
    "Counter",
    "Determiner",
    "Ideophone",
    "Interjection",
    "Noun",
    "Numeral",
    "Participle",
    "Particle",
    "Postposition",
    "Preposition",
    "Pronoun",
    "Proper noun",
    "Verb",
    "Circumfix",
    "Combining form",
    "Infix",
    "Interfix",
    "Prefix",
    "Root",
    "Suffix",
    "Diacritical mark",
    "Letter",
    "Ligature",
    "Number",
    "Punctuation mark",
    "Syllable",
    "Symbol",
    "Phrase",
    "Proverb",
    "Prepositional phrase",
    "Han character",
    "Hanzi",
    "Kanji",
    "Hanja",
    "Romanization",
]


def _warn(word, msg):
    _logger.warning(f"[Warning] {word.word_form}: {msg}")


class WordValidationException(BaseException):
    pass


TESTS = []


def test(f):
    TESTS.append(f)
    return f


@test
def _at_least_one_definition(word: Word):
    if not len(word.definitions) > 0:
        raise WordValidationException(f'word "{word.word_form}" has no definitions')


@test
def _valid_part_of_speech(word: Word):
    for d in word.definitions:
        if d.part_of_speech not in VALID_POS:
            _warn(
                word,
                f'Part of speech "{d.part_of_speech}" is not recognized by Wiktionary. '
                f"Consult the official list: https://en.wiktionary.org/wiki/Wiktionary:Entry_layout#Part_of_speech",
            )


@test
def _ipa_is_bracketed(word: Word):
    for p in word.pronunciations:
        if p.notation.lower() != "ipa":
            continue
        pp = p.pronunciation.strip()
        if not ((pp[0] == "/" and pp[-1] == "/") or (pp[0] == "[" and pp[-1] == "]")):
            _warn(
                word,
                f"IPA should be surrounded by [square brackets] for phonetic transcription or /forward "
                "slashes/ for phonemic transcription",
            )


def validate_word(word: Word):
    for testf in TESTS:
        testf(word)


def validate_words(words: List[Word], lang_code: str, lang_name: str):
    for word in words:
        validate_word(word)

# TODO:
# - validate language code?
# - validate language name?

