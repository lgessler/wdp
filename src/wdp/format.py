from typing import List, Tuple
import re
from wdp.models import Word
from jinja2 import Template

# TODO: add IPA handling e.g. {{IPA|en|foo|bar}}
ENTRY_TEMPLATE = Template(
    """=={{lang_name}}==
{% for word in words %}
{% if words|length > 1 %}
{{ section(1, "Etymology " ~ loop.index) }}
{% endif %}

{% if word['alternate_forms'] %}
{{ section(2, "Alternative forms") }}
{% for form in word['alternate_forms'] %}
* {{'{{'}}alter|{{lang_code}}|{{form.alternate_form}}|{{form.description_of_use}}{{'}}'}}
{% endfor %}
{% endif %}

{% if word['pronunciations'] %}
{{ section(2, "Pronunciations") }}
{% for pronunciation in word['pronunciations'] %}
* {{pronunciation.pronunciation}}
{% endfor %}
{% endif %}

{% for pos in word["grouped_definitions"] %}
{{ section(2, pos) }}
{{'{{'}}head|{{lang_code}}|{{pos}}{{'}}'}}
{% for definition in word["grouped_definitions"][pos] %} 
# {{definition.definition}}{% endfor %}{% endfor %}
{% endfor %}
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
        # a Word will in general have many definitions with different parts of speech--separate them
        word_context["grouped_definitions"] = group_definitions_by_pos(word_context)
        context["words"].append(word_context)

    def section(depth, content):
        """
        Formats string according to whether there is more than one word group or not.
        Args:
            depth:   1-indexed depth relative to the 2-deep ==Language== header
            content: a string to be displayed in a header

        Returns: Formatted string
        """
        c = 1 + (len(word_group) > 1)
        s = '=' * (depth + c)
        return s + content + s

    output = ENTRY_TEMPLATE.render(section=section, **context)
    output = re.sub(r"\n\n+", "\n\n", output)
    output = re.sub(r"===\n\n", "===\n", output)
    return word_group[0].word_form, output


def group_words(words: List[Word]) -> List[List[Word]]:
    """ Group words based on their word_form attribute """
    word_forms = set(w.word_form for w in words)
    return [[w for w in words if w.word_form == word_form] for word_form in word_forms]


def format_entries(words: List[Word], lang_code: str, lang_name: str) -> List[Tuple[str, str]]:
    grouped_words = group_words(words)
    formatted_entries = [format_entry(word_group, lang_code, lang_name) for word_group in grouped_words]
    return formatted_entries
