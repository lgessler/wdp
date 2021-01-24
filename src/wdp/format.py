from typing import List, Tuple
import re
from wdp.models import Word
from jinja2 import Template

# TODO: add IPA handling e.g. {{IPA|en|foo|bar}}
ENTRY_TEMPLATE = Template(
    """=={{lang_name}}==
{% if alternate_forms %}
===Alternative forms===
{% for form in alternate_forms %}
* {{'{{'}}alter|{{lang_code}}|{{form.alternate_form}}|{{form.description_of_use}}{{'}}'}}
{% endfor %}
{% endif %}

{% if pronunciations %}
===Pronunciations===
{% for pronunciation in pronunciations %}
* {{pronunciation.pronunciation}}
{% endfor %}
{% endif %}

{% if words|length > 1 %}
{% for word in words %}
===Etymology {{loop.index}}===
{% for pos in word["grouped_definitions"] %}
===={{pos}}====
{{'{{'}}head|{{lang_code}}|{{pos}}{{'}}'}}
{% for definition in word["grouped_definitions"][pos] %} 
# {{definition.definition}}{% endfor %}{% endfor %}
{% endfor %}
{% else %}
{% for word in words %}
{% for pos in word["grouped_definitions"] %}
===={{pos}}====
{{'{{'}}head|{{lang_code}}|{{pos}}{{'}}'}}
{% for definition in word["grouped_definitions"][pos] %} 
# {{definition.definition}}{% endfor %}{% endfor %}
{% endfor %}
{% endif %}
"""
)


def group_definitions_by_pos(context: dict):
    """
    Return a dict mapping from part of speech to a list of all the definitions with that part of speech.
    """
    definitions = context["definitions"]
    parts_of_speech = set(definition["part_of_speech"] for definition in definitions)

    return {
        pos.capitalize(): [d for d in definitions if d["part_of_speech"] == pos] for pos in parts_of_speech
    }


def build_top_context(context: dict, word_context: dict):
    """
    Most Word information is applies to the whole entry, not being tied to a specific etymology.
    This function pulls this information out of word contexts and add it to the top-level context
    """
    for key in ["pronunciations", "alternate_forms"]:
        context[key] += word_context[key]


def format_entry(word_group: List[Word], lang_code: str, lang_name: str) -> Tuple[str, str]:
    """
    Turn a list of Word objects into Wikitext.
    """
    # the dict we will use to render the jinja template
    context = dict(
        lang_code=lang_code,
        lang_name=lang_name,
        pronunciations=[],
        alternate_forms=[],
        words=[],
    )

    # iterate over Word objects
    for word in word_group:
        word_context = word.to_dict()
        build_top_context(context, word_context)
        # a Word will in general have many definitions with different parts of speech--separate them
        word_context["grouped_definitions"] = group_definitions_by_pos(word_context)
        context["words"].append(word_context)

    output = ENTRY_TEMPLATE.render(**context)
    output = re.sub(r"\n\n+", "\n\n", output)
    output = re.sub(r"===\n\n", "===\n", output)
    return word_group[0].word_form, output


def group_words(words: List[Word]) -> List[List[Word]]:
    """ Group words based on their word_form attribute """
    word_forms = set(w.word_form for w in words)
    return [[w for w in words if w.word_form == word_form] for word_form in word_forms]


def format_entries(words: List[Word], lang_code: str, lang_name: str) -> List[Tuple[str, str]]:
    # TODO: need to find entries with the same form and make sure we add Etymology 1, Etymology 2, etc.
    grouped_words = group_words(words)
    formatted_entries = [format_entry(word_group, lang_code, lang_name) for word_group in grouped_words]
    return formatted_entries
